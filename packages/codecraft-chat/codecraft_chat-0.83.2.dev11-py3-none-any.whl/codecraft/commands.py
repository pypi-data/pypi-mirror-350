import glob
import os
import re
import subprocess
import sys
import tempfile
import datetime
from collections import OrderedDict, defaultdict
from os.path import expanduser
from pathlib import Path

import pyperclip
from PIL import Image, ImageGrab
from prompt_toolkit.completion import Completion, PathCompleter
from prompt_toolkit.document import Document

from codecraft import models, prompts, voice
from codecraft.editor import pipe_editor
from codecraft.format_settings import format_settings
from codecraft.help import Help, install_help_extra
from codecraft.io import CommandCompletionException
from codecraft.llm import litellm
from codecraft.repo import ANY_GIT_ERROR
from codecraft.run_cmd import run_cmd
from codecraft.scrape import Scraper, install_playwright
from codecraft.utils import is_image_file

from .dump import dump  # noqa: F401


class SwitchCoder(Exception):
    def __init__(self, placeholder=None, **kwargs):
        self.kwargs = kwargs
        self.placeholder = placeholder


class Commands:
    voice = None
    scraper = None

    def clone(self):
        return Commands(
            self.io,
            None,
            voice_language=self.voice_language,
            verify_ssl=self.verify_ssl,
            args=self.args,
            parser=self.parser,
            verbose=self.verbose,
            editor=self.editor,
            original_read_only_fnames=self.original_read_only_fnames,
        )

    def __init__(
        self,
        io,
        coder,
        voice_language=None,
        voice_input_device=None,
        voice_format=None,
        verify_ssl=True,
        args=None,
        parser=None,
        verbose=False,
        editor=None,
        original_read_only_fnames=None,
    ):
        self.io = io
        self.coder = coder
        self.parser = parser
        self.args = args
        self.verbose = verbose

        self.verify_ssl = verify_ssl
        if voice_language == "auto":
            voice_language = None

        self.voice_language = voice_language
        self.voice_format = voice_format
        self.voice_input_device = voice_input_device

        self.help = None
        self.editor = editor

        # Store the original read-only filenames provided via args.read
        self.original_read_only_fnames = set(original_read_only_fnames or [])

    def cmd_model(self, args):
        "Switch the Main Model to a new LLM"

        model_name = args.strip()
        
        # If no model name provided, list all available models
        if not model_name:
            return self.cmd_models("")
        
        model = models.Model(
            model_name,
            editor_model=self.coder.main_model.editor_model.name,
            weak_model=self.coder.main_model.weak_model.name,
        )
        models.sanity_check_models(self.io, model)

        # Check if the current edit format is the default for the old model
        old_model_edit_format = self.coder.main_model.edit_format
        current_edit_format = self.coder.edit_format

        new_edit_format = current_edit_format
        if current_edit_format == old_model_edit_format:
            # If the user was using the old model's default, switch to the new model's default
            new_edit_format = model.edit_format

        raise SwitchCoder(main_model=model, edit_format=new_edit_format)

    def cmd_editor_model(self, args):
        "Switch the Editor Model to a new LLM"

        model_name = args.strip()
        model = models.Model(
            self.coder.main_model.name,
            editor_model=model_name,
            weak_model=self.coder.main_model.weak_model.name,
        )
        models.sanity_check_models(self.io, model)
        raise SwitchCoder(main_model=model)

    def cmd_weak_model(self, args):
        "Switch the Weak Model to a new LLM"

        model_name = args.strip()
        model = models.Model(
            self.coder.main_model.name,
            editor_model=self.coder.main_model.editor_model.name,
            weak_model=model_name,
        )
        models.sanity_check_models(self.io, model)
        raise SwitchCoder(main_model=model)

    def cmd_chat_mode(self, args):
        "Switch to a new chat mode"

        from codecraft import coders

        ef = args.strip()
        valid_formats = OrderedDict(
            sorted(
                (
                    coder.edit_format,
                    coder.__doc__.strip().split("\n")[0] if coder.__doc__ else "No description",
                )
                for coder in coders.__all__
                if getattr(coder, "edit_format", None)
            )
        )

        show_formats = OrderedDict(
            [
                ("help", "Get help about using codecraft (usage, config, troubleshoot)."),
                ("ask", "Ask questions about your code without making any changes."),
                ("code", "Ask for changes to your code (using the best edit format)."),
                (
                    "architect",
                    (
                        "Work with an architect model to design code changes, and an editor to make"
                        " them."
                    ),
                ),
                (
                    "context",
                    "Automatically identify which files will need to be edited.",
                ),
            ]
        )

        if ef not in valid_formats and ef not in show_formats:
            if ef:
                self.io.tool_error(f'Chat mode "{ef}" should be one of these:\n')
            else:
                self.io.tool_output("Chat mode should be one of these:\n")

            max_format_length = max(len(format) for format in valid_formats.keys())
            for format, description in show_formats.items():
                self.io.tool_output(f"- {format:<{max_format_length}} : {description}")

            self.io.tool_output("\nOr a valid edit format:\n")
            for format, description in valid_formats.items():
                if format not in show_formats:
                    self.io.tool_output(f"- {format:<{max_format_length}} : {description}")

            return

        summarize_from_coder = True
        edit_format = ef

        if ef == "code":
            edit_format = self.coder.main_model.edit_format
            summarize_from_coder = False
        elif ef == "ask":
            summarize_from_coder = False

        raise SwitchCoder(
            edit_format=edit_format,
            summarize_from_coder=summarize_from_coder,
        )

    def completions_model(self):
        models = litellm.model_cost.keys()
        return models

    def cmd_models(self, args):
        "Search the list of available models"

        args = args.strip()

        if args:
            models.print_matching_models(self.io, args)
        else:
            # List all available models when no argument is provided
            models.print_matching_models(self.io, "")

    def cmd_web(self, args, return_content=False):
        "Scrape a webpage, convert to markdown and send in a message"

        url = args.strip()
        if not url:
            self.io.tool_error("Please provide a URL to scrape.")
            return

        self.io.tool_output(f"Scraping {url}...")
        if not self.scraper:
            disable_playwright = getattr(self.args, "disable_playwright", False)
            if disable_playwright:
                res = False
            else:
                res = install_playwright(self.io)
                if not res:
                    self.io.tool_warning("Unable to initialize playwright.")

            self.scraper = Scraper(
                print_error=self.io.tool_error,
                playwright_available=res,
                verify_ssl=self.verify_ssl,
            )

        content = self.scraper.scrape(url) or ""
        content = f"Here is the content of {url}:\n\n" + content
        if return_content:
            return content

        self.io.tool_output("... added to chat.")

        self.coder.cur_messages += [
            dict(role="user", content=content),
            dict(role="assistant", content="Ok."),
        ]

    def is_command(self, inp):
        return inp[0] in "/!"

    def get_raw_completions(self, cmd):
        assert cmd.startswith("/")
        cmd = cmd[1:]
        cmd = cmd.replace("-", "_")

        raw_completer = getattr(self, f"completions_raw_{cmd}", None)
        return raw_completer

    def get_completions(self, cmd):
        assert cmd.startswith("/")
        cmd = cmd[1:]

        cmd = cmd.replace("-", "_")
        fun = getattr(self, f"completions_{cmd}", None)
        if not fun:
            return
        return sorted(fun())

    def get_commands(self):
        commands = []
        for attr in dir(self):
            if not attr.startswith("cmd_"):
                continue
            cmd = attr[4:]
            cmd = cmd.replace("_", "-")
            commands.append("/" + cmd)

        return commands

    def do_run(self, cmd_name, args):
        cmd_name = cmd_name.replace("-", "_")
        cmd_method_name = f"cmd_{cmd_name}"
        cmd_method = getattr(self, cmd_method_name, None)
        if not cmd_method:
            self.io.tool_output(f"Error: Command {cmd_name} not found.")
            return

        try:
            return cmd_method(args)
        except ANY_GIT_ERROR as err:
            self.io.tool_error(f"Unable to complete {cmd_name}: {err}")

    def matching_commands(self, inp):
        words = inp.strip().split()
        if not words:
            return

        first_word = words[0]
        rest_inp = inp[len(words[0]) :].strip()

        all_commands = self.get_commands()
        matching_commands = [cmd for cmd in all_commands if cmd.startswith(first_word)]
        return matching_commands, first_word, rest_inp

    def run(self, inp):
        if inp.startswith("!"):
            self.coder.event("command_run")
            return self.do_run("run", inp[1:])

        res = self.matching_commands(inp)
        if res is None:
            return
        matching_commands, first_word, rest_inp = res
        if len(matching_commands) == 1:
            command = matching_commands[0][1:]
            self.coder.event(f"command_{command}")
            return self.do_run(command, rest_inp)
        elif first_word in matching_commands:
            command = first_word[1:]
            self.coder.event(f"command_{command}")
            return self.do_run(command, rest_inp)
        elif len(matching_commands) > 1:
            self.io.tool_error(f"Ambiguous command: {', '.join(matching_commands)}")
        else:
            self.io.tool_error(f"Invalid command: {first_word}")

    # any method called cmd_xxx becomes a command automatically.
    # each one must take an args param.

    def cmd_commit(self, args=None):
        "Commit edits to the repo made outside the chat (commit message optional)"
        try:
            self.raw_cmd_commit(args)
        except ANY_GIT_ERROR as err:
            self.io.tool_error(f"Unable to complete commit: {err}")

    def raw_cmd_commit(self, args=None):
        if not self.coder.repo:
            self.io.tool_error("No git repository found.")
            return

        if not self.coder.repo.is_dirty():
            self.io.tool_warning("No more changes to commit.")
            return

        commit_message = args.strip() if args else None
        self.coder.repo.commit(message=commit_message)

    def cmd_lint(self, args="", fnames=None):
        "Lint and fix in-chat files or all dirty files if none in chat"

        if not self.coder.repo:
            self.io.tool_error("No git repository found.")
            return

        if not fnames:
            fnames = self.coder.get_inchat_relative_files()

        # If still no files, get all dirty files in the repo
        if not fnames and self.coder.repo:
            fnames = self.coder.repo.get_dirty_files()

        if not fnames:
            self.io.tool_warning("No dirty files to lint.")
            return

        fnames = [self.coder.abs_root_path(fname) for fname in fnames]

        lint_coder = None
        for fname in fnames:
            try:
                errors = self.coder.linter.lint(fname)
            except FileNotFoundError as err:
                self.io.tool_error(f"Unable to lint {fname}")
                self.io.tool_output(str(err))
                continue

            if not errors:
                continue

            self.io.tool_output(errors)
            if not self.io.confirm_ask(f"Fix lint errors in {fname}?", default="y"):
                continue

            # Commit everything before we start fixing lint errors
            if self.coder.repo.is_dirty() and self.coder.dirty_commits:
                self.cmd_commit("")

            if not lint_coder:
                lint_coder = self.coder.clone(
                    # Clear the chat history, fnames
                    cur_messages=[],
                    done_messages=[],
                    fnames=None,
                )

            lint_coder.add_rel_fname(fname)
            lint_coder.run(errors)
            lint_coder.abs_fnames = set()

        if lint_coder and self.coder.repo.is_dirty() and self.coder.auto_commits:
            self.cmd_commit("")

    def cmd_clear(self, args):
        "Clear the chat history"

        self._clear_chat_history()

    def _drop_all_files(self):
        self.coder.abs_fnames = set()

        # When dropping all files, keep those that were originally provided via args.read
        if self.original_read_only_fnames:
            # Keep only the original read-only files
            to_keep = set()
            for abs_fname in self.coder.abs_read_only_fnames:
                rel_fname = self.coder.get_rel_fname(abs_fname)
                if (
                    abs_fname in self.original_read_only_fnames
                    or rel_fname in self.original_read_only_fnames
                ):
                    to_keep.add(abs_fname)
            self.coder.abs_read_only_fnames = to_keep
        else:
            self.coder.abs_read_only_fnames = set()

    def _clear_chat_history(self):
        self.coder.done_messages = []
        self.coder.cur_messages = []

    def cmd_reset(self, args):
        "Drop all files and clear the chat history"
        self._drop_all_files()
        self._clear_chat_history()
        self.io.tool_output("All files dropped and chat history cleared.")

    def cmd_tokens(self, args):
        "Report on the number of tokens used by the current chat context"

        res = []

        self.coder.choose_fence()

        # system messages
        main_sys = self.coder.fmt_system_prompt(self.coder.gpt_prompts.main_system)
        main_sys += "\n" + self.coder.fmt_system_prompt(self.coder.gpt_prompts.system_reminder)
        msgs = [
            dict(role="system", content=main_sys),
            dict(
                role="system",
                content=self.coder.fmt_system_prompt(self.coder.gpt_prompts.system_reminder),
            ),
        ]

        tokens = self.coder.main_model.token_count(msgs)
        res.append((tokens, "system messages", ""))

        # chat history
        msgs = self.coder.done_messages + self.coder.cur_messages
        if msgs:
            tokens = self.coder.main_model.token_count(msgs)
            res.append((tokens, "chat history", "use /clear to clear"))

        # repo map
        other_files = set(self.coder.get_all_abs_files()) - set(self.coder.abs_fnames)
        if self.coder.repo_map:
            repo_content = self.coder.repo_map.get_repo_map(self.coder.abs_fnames, other_files)
            if repo_content:
                tokens = self.coder.main_model.token_count(repo_content)
                res.append((tokens, "repository map", "use --map-tokens to resize"))

        fence = "`" * 3

        file_res = []
        # files
        for fname in self.coder.abs_fnames:
            relative_fname = self.coder.get_rel_fname(fname)
            content = self.io.read_text(fname)
            if is_image_file(relative_fname):
                tokens = self.coder.main_model.token_count_for_image(fname)
            else:
                # approximate
                content = f"{relative_fname}\n{fence}\n" + content + "{fence}\n"
                tokens = self.coder.main_model.token_count(content)
            file_res.append((tokens, f"{relative_fname}", "/drop to remove"))

        # read-only files
        for fname in self.coder.abs_read_only_fnames:
            relative_fname = self.coder.get_rel_fname(fname)
            content = self.io.read_text(fname)
            if content is not None and not is_image_file(relative_fname):
                # approximate
                content = f"{relative_fname}\n{fence}\n" + content + "{fence}\n"
                tokens = self.coder.main_model.token_count(content)
                file_res.append((tokens, f"{relative_fname} (read-only)", "/drop to remove"))

        file_res.sort()
        res.extend(file_res)

        self.io.tool_output(
            f"Approximate context window usage for {self.coder.main_model.name}, in tokens:"
        )
        self.io.tool_output()

        width = 8
        cost_width = 9

        def fmt(v):
            return format(int(v), ",").rjust(width)

        col_width = max(len(row[1]) for row in res)

        cost_pad = " " * cost_width
        total = 0
        total_cost = 0.0
        for tk, msg, tip in res:
            total += tk
            cost = tk * (self.coder.main_model.info.get("input_cost_per_token") or 0)
            total_cost += cost
            msg = msg.ljust(col_width)
            self.io.tool_output(f"${cost:7.4f} {fmt(tk)} {msg} {tip}")  # noqa: E231

        self.io.tool_output("=" * (width + cost_width + 1))
        self.io.tool_output(f"${total_cost:7.4f} {fmt(total)} tokens total")  # noqa: E231

        limit = self.coder.main_model.info.get("max_input_tokens") or 0
        if not limit:
            return

        remaining = limit - total
        if remaining > 1024:
            self.io.tool_output(f"{cost_pad}{fmt(remaining)} tokens remaining in context window")
        elif remaining > 0:
            self.io.tool_error(
                f"{cost_pad}{fmt(remaining)} tokens remaining in context window (use /drop or"
                " /clear to make space)"
            )
        else:
            self.io.tool_error(
                f"{cost_pad}{fmt(remaining)} tokens remaining, window exhausted (use /drop or"
                " /clear to make space)"
            )
        self.io.tool_output(f"{cost_pad}{fmt(limit)} tokens max context window size")

    def cmd_undo(self, args):
        "Undo the last git commit if it was done by codecraft"
        try:
            self.raw_cmd_undo(args)
        except ANY_GIT_ERROR as err:
            self.io.tool_error(f"Unable to complete undo: {err}")

    def raw_cmd_undo(self, args):
        if not self.coder.repo:
            self.io.tool_error("No git repository found.")
            return

        last_commit = self.coder.repo.get_head_commit()
        if not last_commit or not last_commit.parents:
            self.io.tool_error("This is the first commit in the repository. Cannot undo.")
            return

        last_commit_hash = self.coder.repo.get_head_commit_sha(short=True)
        last_commit_message = self.coder.repo.get_head_commit_message("(unknown)").strip()
        if last_commit_hash not in self.coder.codecraft_commit_hashes:
            self.io.tool_error("The last commit was not made by codecraft in this chat session.")
            self.io.tool_output(
                "You could try `/git reset --hard HEAD^` but be aware that this is a destructive"
                " command!"
            )
            return

        if len(last_commit.parents) > 1:
            self.io.tool_error(
                f"The last commit {last_commit.hexsha} has more than 1 parent, can't undo."
            )
            return

        prev_commit = last_commit.parents[0]
        changed_files_last_commit = [item.a_path for item in last_commit.diff(prev_commit)]

        for fname in changed_files_last_commit:
            if self.coder.repo.repo.is_dirty(path=fname):
                self.io.tool_error(
                    f"The file {fname} has uncommitted changes. Please stash them before undoing."
                )
                return

            # Check if the file was in the repo in the previous commit
            try:
                prev_commit.tree[fname]
            except KeyError:
                self.io.tool_error(
                    f"The file {fname} was not in the repository in the previous commit. Cannot"
                    " undo safely."
                )
                return

        local_head = self.coder.repo.repo.git.rev_parse("HEAD")
        current_branch = self.coder.repo.repo.active_branch.name
        try:
            remote_head = self.coder.repo.repo.git.rev_parse(f"origin/{current_branch}")
            has_origin = True
        except ANY_GIT_ERROR:
            has_origin = False

        if has_origin:
            if local_head == remote_head:
                self.io.tool_error(
                    "The last commit has already been pushed to the origin. Undoing is not"
                    " possible."
                )
                return

        # Reset only the files which are part of `last_commit`
        restored = set()
        unrestored = set()
        for file_path in changed_files_last_commit:
            try:
                self.coder.repo.repo.git.checkout("HEAD~1", file_path)
                restored.add(file_path)
            except ANY_GIT_ERROR:
                unrestored.add(file_path)

        if unrestored:
            self.io.tool_error(f"Error restoring {file_path}, aborting undo.")
            self.io.tool_output("Restored files:")
            for file in restored:
                self.io.tool_output(f"  {file}")
            self.io.tool_output("Unable to restore files:")
            for file in unrestored:
                self.io.tool_output(f"  {file}")
            return

        # Move the HEAD back before the latest commit
        self.coder.repo.repo.git.reset("--soft", "HEAD~1")

        self.io.tool_output(f"Removed: {last_commit_hash} {last_commit_message}")

        # Get the current HEAD after undo
        current_head_hash = self.coder.repo.get_head_commit_sha(short=True)
        current_head_message = self.coder.repo.get_head_commit_message("(unknown)").strip()
        self.io.tool_output(f"Now at:  {current_head_hash} {current_head_message}")

        if self.coder.main_model.send_undo_reply:
            return prompts.undo_command_reply

    def cmd_diff(self, args=""):
        "Display the diff of changes since the last message"
        try:
            self.raw_cmd_diff(args)
        except ANY_GIT_ERROR as err:
            self.io.tool_error(f"Unable to complete diff: {err}")

    def raw_cmd_diff(self, args=""):
        if not self.coder.repo:
            self.io.tool_error("No git repository found.")
            return

        current_head = self.coder.repo.get_head_commit_sha()
        if current_head is None:
            self.io.tool_error("Unable to get current commit. The repository might be empty.")
            return

        if len(self.coder.commit_before_message) < 2:
            commit_before_message = current_head + "^"
        else:
            commit_before_message = self.coder.commit_before_message[-2]

        if not commit_before_message or commit_before_message == current_head:
            self.io.tool_warning("No changes to display since the last message.")
            return

        self.io.tool_output(f"Diff since {commit_before_message[:7]}...")

        if self.coder.pretty:
            run_cmd(f"git diff {commit_before_message}")
            return

        diff = self.coder.repo.diff_commits(
            self.coder.pretty,
            commit_before_message,
            "HEAD",
        )

        self.io.print(diff)

    def quote_fname(self, fname):
        if " " in fname and '"' not in fname:
            fname = f'"{fname}"'
        return fname

    def completions_raw_read_only(self, document, complete_event):
        # Get the text before the cursor
        text = document.text_before_cursor

        # Skip the first word and the space after it
        after_command = text.split()[-1]

        # Create a new Document object with the text after the command
        new_document = Document(after_command, cursor_position=len(after_command))

        def get_paths():
            return [self.coder.root] if self.coder.root else None

        path_completer = PathCompleter(
            get_paths=get_paths,
            only_directories=False,
            expanduser=True,
        )

        # Adjust the start_position to replace all of 'after_command'
        adjusted_start_position = -len(after_command)

        # Collect all completions
        all_completions = []

        # Iterate over the completions and modify them
        for completion in path_completer.get_completions(new_document, complete_event):
            quoted_text = self.quote_fname(after_command + completion.text)
            all_completions.append(
                Completion(
                    text=quoted_text,
                    start_position=adjusted_start_position,
                    display=completion.display,
                    style=completion.style,
                    selected_style=completion.selected_style,
                )
            )

        # Add completions from the 'add' command
        add_completions = self.completions_add()
        for completion in add_completions:
            if after_command in completion:
                all_completions.append(
                    Completion(
                        text=completion,
                        start_position=adjusted_start_position,
                        display=completion,
                    )
                )

        # Sort all completions based on their text
        sorted_completions = sorted(all_completions, key=lambda c: c.text)

        # Yield the sorted completions
        for completion in sorted_completions:
            yield completion

    def completions_add(self):
        files = set(self.coder.get_all_relative_files())
        files = files - set(self.coder.get_inchat_relative_files())
        files = [self.quote_fname(fn) for fn in files]
        return files

    def glob_filtered_to_repo(self, pattern):
        if not pattern.strip():
            return []
        try:
            if os.path.isabs(pattern):
                # Handle absolute paths
                raw_matched_files = [Path(pattern)]
            else:
                try:
                    raw_matched_files = list(Path(self.coder.root).glob(pattern))
                except (IndexError, AttributeError):
                    raw_matched_files = []
        except ValueError as err:
            self.io.tool_error(f"Error matching {pattern}: {err}")
            raw_matched_files = []

        matched_files = []
        for fn in raw_matched_files:
            matched_files += expand_subdir(fn)

        matched_files = [
            fn.relative_to(self.coder.root)
            for fn in matched_files
            if fn.is_relative_to(self.coder.root)
        ]

        # if repo, filter against it
        if self.coder.repo:
            git_files = self.coder.repo.get_tracked_files()
            matched_files = [fn for fn in matched_files if str(fn) in git_files]

        res = list(map(str, matched_files))
        return res

    def cmd_add(self, args):
        "Add files to the chat so codecraft can edit them or review them in detail"

        all_matched_files = set()

        filenames = parse_quoted_filenames(args)
        for word in filenames:
            if Path(word).is_absolute():
                fname = Path(word)
            else:
                fname = Path(self.coder.root) / word

            if self.coder.repo and self.coder.repo.ignored_file(fname):
                self.io.tool_warning(f"Skipping {fname} due to codecraftignore or --subtree-only.")
                continue

            if fname.exists():
                if fname.is_file():
                    all_matched_files.add(str(fname))
                    continue
                # an existing dir, escape any special chars so they won't be globs
                word = re.sub(r"([\*\?\[\]])", r"[\1]", word)

            matched_files = self.glob_filtered_to_repo(word)
            if matched_files:
                all_matched_files.update(matched_files)
                continue

            if "*" in str(fname) or "?" in str(fname):
                self.io.tool_error(
                    f"No match, and cannot create file with wildcard characters: {fname}"
                )
                continue

            if fname.exists() and fname.is_dir() and self.coder.repo:
                self.io.tool_error(f"Directory {fname} is not in git.")
                self.io.tool_output(f"You can add to git with: /git add {fname}")
                continue

            if self.io.confirm_ask(f"No files matched '{word}'. Do you want to create {fname}?"):
                try:
                    fname.parent.mkdir(parents=True, exist_ok=True)
                    fname.touch()
                    all_matched_files.add(str(fname))
                except OSError as e:
                    self.io.tool_error(f"Error creating file {fname}: {e}")

        for matched_file in sorted(all_matched_files):
            abs_file_path = self.coder.abs_root_path(matched_file)

            if not abs_file_path.startswith(self.coder.root) and not is_image_file(matched_file):
                self.io.tool_error(
                    f"Can not add {abs_file_path}, which is not within {self.coder.root}"
                )
                continue

            if self.coder.repo and self.coder.repo.git_ignored_file(matched_file):
                self.io.tool_error(f"Can't add {matched_file} which is in gitignore")
                continue

            if abs_file_path in self.coder.abs_fnames:
                self.io.tool_error(f"{matched_file} is already in the chat as an editable file")
                continue
            elif abs_file_path in self.coder.abs_read_only_fnames:
                if self.coder.repo and self.coder.repo.path_in_repo(matched_file):
                    self.coder.abs_read_only_fnames.remove(abs_file_path)
                    self.coder.abs_fnames.add(abs_file_path)
                    self.io.tool_output(
                        f"Moved {matched_file} from read-only to editable files in the chat"
                    )
                else:
                    self.io.tool_error(
                        f"Cannot add {matched_file} as it's not part of the repository"
                    )
            else:
                if is_image_file(matched_file) and not self.coder.main_model.info.get(
                    "supports_vision"
                ):
                    self.io.tool_error(
                        f"Cannot add image file {matched_file} as the"
                        f" {self.coder.main_model.name} does not support images."
                    )
                    continue
                content = self.io.read_text(abs_file_path)
                if content is None:
                    self.io.tool_error(f"Unable to read {matched_file}")
                else:
                    self.coder.abs_fnames.add(abs_file_path)
                    fname = self.coder.get_rel_fname(abs_file_path)
                    self.io.tool_output(f"Added {fname} to the chat")
                    self.coder.check_added_files()

    def completions_drop(self):
        files = self.coder.get_inchat_relative_files()
        read_only_files = [self.coder.get_rel_fname(fn) for fn in self.coder.abs_read_only_fnames]
        all_files = files + read_only_files
        all_files = [self.quote_fname(fn) for fn in all_files]
        return all_files

    def cmd_drop(self, args=""):
        "Remove files from the chat session to free up context space"

        if not args.strip():
            if self.original_read_only_fnames:
                self.io.tool_output(
                    "Dropping all files from the chat session except originally read-only files."
                )
            else:
                self.io.tool_output("Dropping all files from the chat session.")
            self._drop_all_files()
            return

        filenames = parse_quoted_filenames(args)
        for word in filenames:
            # Expand tilde in the path
            expanded_word = os.path.expanduser(word)

            # Handle read-only files with substring matching and samefile check
            read_only_matched = []
            for f in self.coder.abs_read_only_fnames:
                if expanded_word in f:
                    read_only_matched.append(f)
                    continue

                # Try samefile comparison for relative paths
                try:
                    abs_word = os.path.abspath(expanded_word)
                    if os.path.samefile(abs_word, f):
                        read_only_matched.append(f)
                except (FileNotFoundError, OSError):
                    continue

            for matched_file in read_only_matched:
                self.coder.abs_read_only_fnames.remove(matched_file)
                self.io.tool_output(f"Removed read-only file {matched_file} from the chat")

            # For editable files, use glob if word contains glob chars, otherwise use substring
            if any(c in expanded_word for c in "*?[]"):
                matched_files = self.glob_filtered_to_repo(expanded_word)
            else:
                # Use substring matching like we do for read-only files
                matched_files = [
                    self.coder.get_rel_fname(f) for f in self.coder.abs_fnames if expanded_word in f
                ]

            if not matched_files:
                matched_files.append(expanded_word)

            for matched_file in matched_files:
                abs_fname = self.coder.abs_root_path(matched_file)
                if abs_fname in self.coder.abs_fnames:
                    self.coder.abs_fnames.remove(abs_fname)
                    self.io.tool_output(f"Removed {matched_file} from the chat")

    def cmd_git(self, args):
        "Run a git command (output excluded from chat)"
        combined_output = None
        try:
            args = "git " + args
            env = dict(subprocess.os.environ)
            env["GIT_EDITOR"] = "true"
            result = subprocess.run(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                shell=True,
                encoding=self.io.encoding,
                errors="replace",
            )
            combined_output = result.stdout
        except Exception as e:
            self.io.tool_error(f"Error running /git command: {e}")

        if combined_output is None:
            return

        self.io.tool_output(combined_output)

    def cmd_test(self, args):
        "Run a shell command and add the output to the chat on non-zero exit code"
        if not args and self.coder.test_cmd:
            args = self.coder.test_cmd

        if not args:
            return

        if not callable(args):
            if type(args) is not str:
                raise ValueError(repr(args))
            return self.cmd_run(args, True)

        errors = args()
        if not errors:
            return

        self.io.tool_output(errors)
        return errors

    def cmd_run(self, args, add_on_nonzero_exit=False):
        "Run a shell command and optionally add the output to the chat (alias: !)"
        exit_status, combined_output = run_cmd(
            args, verbose=self.verbose, error_print=self.io.tool_error, cwd=self.coder.root
        )

        if combined_output is None:
            return

        # Calculate token count of output
        token_count = self.coder.main_model.token_count(combined_output)
        k_tokens = token_count / 1000

        if add_on_nonzero_exit:
            add = exit_status != 0
        else:
            add = self.io.confirm_ask(f"Add {k_tokens:.1f}k tokens of command output to the chat?")

        if add:
            num_lines = len(combined_output.strip().splitlines())
            line_plural = "line" if num_lines == 1 else "lines"
            self.io.tool_output(f"Added {num_lines} {line_plural} of output to the chat.")

            msg = prompts.run_output.format(
                command=args,
                output=combined_output,
            )

            self.coder.cur_messages += [
                dict(role="user", content=msg),
                dict(role="assistant", content="Ok."),
            ]

            if add_on_nonzero_exit and exit_status != 0:
                # Return the formatted output message for test failures
                return msg
            elif add and exit_status != 0:
                self.io.placeholder = "What's wrong? Fix"

        # Return None if output wasn't added or command succeeded
        return None

    def cmd_exit(self, args):
        "Exit the application"
        self.coder.event("exit", reason="/exit")
        sys.exit()

    def cmd_quit(self, args):
        "Exit the application"
        self.cmd_exit(args)

    def cmd_ls(self, args):
        "List all known files and indicate which are included in the chat session"

        files = self.coder.get_all_relative_files()

        other_files = []
        chat_files = []
        read_only_files = []
        for file in files:
            abs_file_path = self.coder.abs_root_path(file)
            if abs_file_path in self.coder.abs_fnames:
                chat_files.append(file)
            else:
                other_files.append(file)

        # Add read-only files
        for abs_file_path in self.coder.abs_read_only_fnames:
            rel_file_path = self.coder.get_rel_fname(abs_file_path)
            read_only_files.append(rel_file_path)

        if not chat_files and not other_files and not read_only_files:
            self.io.tool_output("\nNo files in chat, git repo, or read-only list.")
            return

        if other_files:
            self.io.tool_output("Repo files not in the chat:\n")
        for file in other_files:
            self.io.tool_output(f"  {file}")

        if read_only_files:
            self.io.tool_output("\nRead-only files:\n")
        for file in read_only_files:
            self.io.tool_output(f"  {file}")

        if chat_files:
            self.io.tool_output("\nFiles in chat:\n")
        for file in chat_files:
            self.io.tool_output(f"  {file}")

    def basic_help(self):
        commands = sorted(self.get_commands())
        pad = max(len(cmd) for cmd in commands)
        pad = "{cmd:" + str(pad) + "}"
        for cmd in commands:
            cmd_method_name = f"cmd_{cmd[1:]}".replace("-", "_")
            cmd_method = getattr(self, cmd_method_name, None)
            cmd = pad.format(cmd=cmd)
            if cmd_method:
                description = cmd_method.__doc__
                self.io.tool_output(f"{cmd} {description}")
            else:
                self.io.tool_output(f"{cmd} No description available.")
        self.io.tool_output()
        self.io.tool_output("Use `/help <question>` to ask questions about how to use codecraft.")

    def cmd_help(self, args):
        "Ask questions about codecraft"

        if not args.strip():
            self.basic_help()
            return

        self.coder.event("interactive help")
        from codecraft.coders.base_coder import Coder

        if not self.help:
            res = install_help_extra(self.io)
            if not res:
                self.io.tool_error("Unable to initialize interactive help.")
                return

            self.help = Help()

        coder = Coder.create(
            io=self.io,
            from_coder=self.coder,
            edit_format="help",
            summarize_from_coder=False,
            map_tokens=512,
            map_mul_no_files=1,
        )
        user_msg = self.help.ask(args)
        user_msg += """
# Announcement lines from when this session of codecraft was launched:

"""
        user_msg += "\n".join(self.coder.get_announcements()) + "\n"

        coder.run(user_msg, preproc=False)

        if self.coder.repo_map:
            map_tokens = self.coder.repo_map.max_map_tokens
            map_mul_no_files = self.coder.repo_map.map_mul_no_files
        else:
            map_tokens = 0
            map_mul_no_files = 1

        raise SwitchCoder(
            edit_format=self.coder.edit_format,
            summarize_from_coder=False,
            from_coder=coder,
            map_tokens=map_tokens,
            map_mul_no_files=map_mul_no_files,
            show_announcements=False,
        )

    def completions_ask(self):
        raise CommandCompletionException()

    def completions_code(self):
        raise CommandCompletionException()

    def completions_architect(self):
        raise CommandCompletionException()

    def completions_context(self):
        raise CommandCompletionException()

    def cmd_ask(self, args):
        """Ask questions about the code base without editing any files. If no prompt provided, switches to ask mode."""  # noqa
        return self._generic_chat_command(args, "ask")

    def cmd_code(self, args):
        """Ask for changes to your code. If no prompt provided, switches to code mode."""  # noqa
        return self._generic_chat_command(args, self.coder.main_model.edit_format)

    def cmd_architect(self, args):
        """Enter architect/editor mode using 2 different models. If no prompt provided, switches to architect/editor mode."""  # noqa
        return self._generic_chat_command(args, "architect")

    def cmd_context(self, args):
        """Enter context mode to see surrounding code context. If no prompt provided, switches to context mode."""  # noqa
        return self._generic_chat_command(args, "context", placeholder=args.strip() or None)

    def _generic_chat_command(self, args, edit_format, placeholder=None):
        if not args.strip():
            # Switch to the corresponding chat mode if no args provided
            return self.cmd_chat_mode(edit_format)

        from codecraft.coders.base_coder import Coder

        coder = Coder.create(
            io=self.io,
            from_coder=self.coder,
            edit_format=edit_format,
            summarize_from_coder=False,
        )

        user_msg = args
        coder.run(user_msg)

        # Use the provided placeholder if any
        raise SwitchCoder(
            edit_format=self.coder.edit_format,
            summarize_from_coder=False,
            from_coder=coder,
            show_announcements=False,
            placeholder=placeholder,
        )

    def get_help_md(self):
        "Show help about all commands in markdown"

        res = """
|Command|Description|
|:------|:----------|
"""
        commands = sorted(self.get_commands())
        for cmd in commands:
            cmd_method_name = f"cmd_{cmd[1:]}".replace("-", "_")
            cmd_method = getattr(self, cmd_method_name, None)
            if cmd_method:
                description = cmd_method.__doc__
                res += f"| **{cmd}** | {description} |\n"
            else:
                res += f"| **{cmd}** | |\n"

        res += "\n"
        return res

    def cmd_voice(self, args):
        "Record and transcribe voice input"

        if not self.voice:
            if "OPENAI_API_KEY" not in os.environ:
                self.io.tool_error("To use /voice you must provide an OpenAI API key.")
                return
            try:
                self.voice = voice.Voice(
                    audio_format=self.voice_format or "wav", device_name=self.voice_input_device
                )
            except voice.SoundDeviceError:
                self.io.tool_error(
                    "Unable to import `sounddevice` and/or `soundfile`, is portaudio installed?"
                )
                return

        try:
            text = self.voice.record_and_transcribe(None, language=self.voice_language)
        except litellm.OpenAIError as err:
            self.io.tool_error(f"Unable to use OpenAI whisper model: {err}")
            return

        if text:
            self.io.placeholder = text

    def cmd_paste(self, args):
        """Paste image/text from the clipboard into the chat.\
        Optionally provide a name for the image."""
        try:
            # Check for image first
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image):
                if args.strip():
                    filename = args.strip()
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in (".jpg", ".jpeg", ".png"):
                        basename = filename
                    else:
                        basename = f"{filename}.png"
                else:
                    basename = "clipboard_image.png"

                temp_dir = tempfile.mkdtemp()
                temp_file_path = os.path.join(temp_dir, basename)
                image_format = "PNG" if basename.lower().endswith(".png") else "JPEG"
                image.save(temp_file_path, image_format)

                abs_file_path = Path(temp_file_path).resolve()

                # Check if a file with the same name already exists in the chat
                existing_file = next(
                    (f for f in self.coder.abs_fnames if Path(f).name == abs_file_path.name), None
                )
                if existing_file:
                    self.coder.abs_fnames.remove(existing_file)
                    self.io.tool_output(f"Replaced existing image in the chat: {existing_file}")

                self.coder.abs_fnames.add(str(abs_file_path))
                self.io.tool_output(f"Added clipboard image to the chat: {abs_file_path}")
                self.coder.check_added_files()

                return

            # If not an image, try to get text
            text = pyperclip.paste()
            if text:
                self.io.tool_output(text)
                return text

            self.io.tool_error("No image or text content found in clipboard.")
            return

        except Exception as e:
            self.io.tool_error(f"Error processing clipboard content: {e}")

    def cmd_read_only(self, args):
        "Add files to the chat that are for reference only, or turn added files to read-only"
        if not args.strip():
            # Convert all files in chat to read-only
            for fname in list(self.coder.abs_fnames):
                self.coder.abs_fnames.remove(fname)
                self.coder.abs_read_only_fnames.add(fname)
                rel_fname = self.coder.get_rel_fname(fname)
                self.io.tool_output(f"Converted {rel_fname} to read-only")
            return

        filenames = parse_quoted_filenames(args)
        all_paths = []

        # First collect all expanded paths
        for pattern in filenames:
            expanded_pattern = expanduser(pattern)
            if os.path.isabs(expanded_pattern):
                # For absolute paths, glob it
                matches = list(glob.glob(expanded_pattern))
            else:
                # For relative paths and globs, use glob from the root directory
                matches = list(Path(self.coder.root).glob(expanded_pattern))

            if not matches:
                self.io.tool_error(f"No matches found for: {pattern}")
            else:
                all_paths.extend(matches)

        # Then process them in sorted order
        for path in sorted(all_paths):
            abs_path = self.coder.abs_root_path(path)
            if os.path.isfile(abs_path):
                self._add_read_only_file(abs_path, path)
            elif os.path.isdir(abs_path):
                self._add_read_only_directory(abs_path, path)
            else:
                self.io.tool_error(f"Not a file or directory: {abs_path}")

    def _add_read_only_file(self, abs_path, original_name):
        if is_image_file(original_name) and not self.coder.main_model.info.get("supports_vision"):
            self.io.tool_error(
                f"Cannot add image file {original_name} as the"
                f" {self.coder.main_model.name} does not support images."
            )
            return

        if abs_path in self.coder.abs_read_only_fnames:
            self.io.tool_error(f"{original_name} is already in the chat as a read-only file")
            return
        elif abs_path in self.coder.abs_fnames:
            self.coder.abs_fnames.remove(abs_path)
            self.coder.abs_read_only_fnames.add(abs_path)
            self.io.tool_output(
                f"Moved {original_name} from editable to read-only files in the chat"
            )
        else:
            self.coder.abs_read_only_fnames.add(abs_path)
            self.io.tool_output(f"Added {original_name} to read-only files.")

    def _add_read_only_directory(self, abs_path, original_name):
        added_files = 0
        for root, _, files in os.walk(abs_path):
            for file in files:
                file_path = os.path.join(root, file)
                if (
                    file_path not in self.coder.abs_fnames
                    and file_path not in self.coder.abs_read_only_fnames
                ):
                    self.coder.abs_read_only_fnames.add(file_path)
                    added_files += 1

        if added_files > 0:
            self.io.tool_output(
                f"Added {added_files} files from directory {original_name} to read-only files."
            )
        else:
            self.io.tool_output(f"No new files added from directory {original_name}.")

    def cmd_map(self, args):
        "Print out the current repository map"
        repo_map = self.coder.get_repo_map()
        if repo_map:
            self.io.tool_output(repo_map)
        else:
            self.io.tool_output("No repository map available.")

    def cmd_map_refresh(self, args):
        "Force a refresh of the repository map"
        repo_map = self.coder.get_repo_map(force_refresh=True)
        if repo_map:
            self.io.tool_output("The repo map has been refreshed, use /map to view it.")

    def cmd_settings(self, args):
        "Print out the current settings"
        settings = format_settings(self.parser, self.args)
        announcements = "\n".join(self.coder.get_announcements())
        output = f"{announcements}\n{settings}"
        self.io.tool_output(output)

    def completions_raw_load(self, document, complete_event):
        return self.completions_raw_read_only(document, complete_event)

    def cmd_load(self, args):
        "Load and execute commands from a file"
        if not args.strip():
            self.io.tool_error("Please provide a filename containing commands to load.")
            return

        try:
            with open(args.strip(), "r", encoding=self.io.encoding, errors="replace") as f:
                commands = f.readlines()
        except FileNotFoundError:
            self.io.tool_error(f"File not found: {args}")
            return
        except Exception as e:
            self.io.tool_error(f"Error reading file: {e}")
            return

        for cmd in commands:
            cmd = cmd.strip()
            if not cmd or cmd.startswith("#"):
                continue

            self.io.tool_output(f"\nExecuting: {cmd}")
            try:
                self.run(cmd)
            except SwitchCoder:
                self.io.tool_error(
                    f"Command '{cmd}' is only supported in interactive mode, skipping."
                )

    def completions_raw_save(self, document, complete_event):
        return self.completions_raw_read_only(document, complete_event)

    def cmd_save(self, args):
        "Save commands to a file that can reconstruct the current chat session's files"
        if not args.strip():
            self.io.tool_error("Please provide a filename to save the commands to.")
            return

        try:
            with open(args.strip(), "w", encoding=self.io.encoding) as f:
                f.write("/drop\n")
                # Write commands to add editable files
                for fname in sorted(self.coder.abs_fnames):
                    rel_fname = self.coder.get_rel_fname(fname)
                    f.write(f"/add       {rel_fname}\n")

                # Write commands to add read-only files
                for fname in sorted(self.coder.abs_read_only_fnames):
                    # Use absolute path for files outside repo root, relative path for files inside
                    if Path(fname).is_relative_to(self.coder.root):
                        rel_fname = self.coder.get_rel_fname(fname)
                        f.write(f"/read-only {rel_fname}\n")
                    else:
                        f.write(f"/read-only {fname}\n")

            self.io.tool_output(f"Saved commands to {args.strip()}")
        except Exception as e:
            self.io.tool_error(f"Error saving commands to file: {e}")

    def cmd_multiline_mode(self, args):
        "Toggle multiline mode (swaps behavior of Enter and Meta+Enter)"
        self.io.toggle_multiline_mode()

    def cmd_copy(self, args):
        "Copy the last assistant message to the clipboard"
        all_messages = self.coder.done_messages + self.coder.cur_messages
        assistant_messages = [msg for msg in reversed(all_messages) if msg["role"] == "assistant"]

        if not assistant_messages:
            self.io.tool_error("No assistant messages found to copy.")
            return

        last_assistant_message = assistant_messages[0]["content"]

        try:
            pyperclip.copy(last_assistant_message)
            preview = (
                last_assistant_message[:50] + "..."
                if len(last_assistant_message) > 50
                else last_assistant_message
            )
            self.io.tool_output(f"Copied last assistant message to clipboard. Preview: {preview}")
        except pyperclip.PyperclipException as e:
            self.io.tool_error(f"Failed to copy to clipboard: {str(e)}")
            self.io.tool_output(
                "You may need to install xclip or xsel on Linux, or pbcopy on macOS."
            )
        except Exception as e:
            self.io.tool_error(f"An unexpected error occurred while copying to clipboard: {str(e)}")

    def cmd_report(self, args):
        "Report a problem by opening a GitHub Issue"
        from codecraft.report import report_github_issue

        announcements = "\n".join(self.coder.get_announcements())
        issue_text = announcements

        if args.strip():
            title = args.strip()
        else:
            title = None

        report_github_issue(issue_text, title=title, confirm=False)

    def cmd_editor(self, initial_content=""):
        "Open an editor to write a prompt"

        user_input = pipe_editor(initial_content, suffix="md", editor=self.editor)
        if user_input.strip():
            self.io.set_placeholder(user_input.rstrip())

    def cmd_edit(self, args=""):
        "Alias for /editor: Open an editor to write a prompt"
        return self.cmd_editor(args)

    def cmd_think_tokens(self, args):
        "Set the thinking token budget (supports formats like 8096, 8k, 10.5k, 0.5M)"
        model = self.coder.main_model

        if not args.strip():
            # Display current value if no args are provided
            formatted_budget = model.get_thinking_tokens()
            if formatted_budget is None:
                self.io.tool_output("Thinking tokens are not currently set.")
            else:
                budget = model.get_raw_thinking_tokens()
                self.io.tool_output(
                    f"Current thinking token budget: {budget:,} tokens ({formatted_budget})."
                )
            return

        value = args.strip()
        model.set_thinking_tokens(value)

        formatted_budget = model.get_thinking_tokens()
        budget = model.get_raw_thinking_tokens()

        self.io.tool_output(f"Set thinking token budget to {budget:,} tokens ({formatted_budget}).")
        self.io.tool_output()

        # Output announcements
        announcements = "\n".join(self.coder.get_announcements())
        self.io.tool_output(announcements)

    def cmd_reasoning_effort(self, args):
        "Set the reasoning effort level (values: number or low/medium/high depending on model)"
        model = self.coder.main_model

        if not args.strip():
            # Display current value if no args are provided
            reasoning_value = model.get_reasoning_effort()
            if reasoning_value is None:
                self.io.tool_output("Reasoning effort is not currently set.")
            else:
                self.io.tool_output(f"Current reasoning effort: {reasoning_value}")
            return

        value = args.strip()
        model.set_reasoning_effort(value)
        reasoning_value = model.get_reasoning_effort()
        self.io.tool_output(f"Set reasoning effort to {reasoning_value}")
        self.io.tool_output()

        # Output announcements
        announcements = "\n".join(self.coder.get_announcements())
        self.io.tool_output(announcements)

    def cmd_copy_context(self, args=None):
        """Copy the current chat context as markdown, suitable to paste into a web UI"""

        chunks = self.coder.format_chat_chunks()

        markdown = ""

        # Only include specified chunks in order
        for messages in [chunks.repo, chunks.readonly_files, chunks.chat_files]:
            for msg in messages:
                # Only include user messages
                if msg["role"] != "user":
                    continue

                content = msg["content"]

                # Handle image/multipart content
                if isinstance(content, list):
                    for part in content:
                        if part.get("type") == "text":
                            markdown += part["text"] + "\n\n"
                else:
                    markdown += content + "\n\n"

        args = args or ""
        markdown += f"""
Just tell me how to edit the files to make the changes.
Don't give me back entire files.
Just show me the edits I need to make.

{args}
"""

        try:
            pyperclip.copy(markdown)
            self.io.tool_output("Copied code context to clipboard.")
        except pyperclip.PyperclipException as e:
            self.io.tool_error(f"Failed to copy to clipboard: {str(e)}")
            self.io.tool_output(
                "You may need to install xclip or xsel on Linux, or pbcopy on macOS."
            )
        except Exception as e:
            self.io.tool_error(f"An unexpected error occurred while copying to clipboard: {str(e)}")

    def cmd_review(self, args=""):
        "Conduct a comprehensive code review of the entire codebase and generate a TODO report"
        
        # Parse arguments for additional options
        import argparse
        import datetime
        import math
        import os
        
        parser = argparse.ArgumentParser(description="Code review options")
        parser.add_argument("--exclude", help="Glob patterns to exclude, comma-separated (e.g., 'tests/*,docs/*')")
        parser.add_argument("--include", help="Glob patterns to include, comma-separated (e.g., 'src/*.py')")
        parser.add_argument("--max-files", type=int, help="Maximum number of files to review")
        parser.add_argument("--focus", help="Aspects to focus on (e.g., 'security,performance')")
        parser.add_argument("--output", help="Output file path (default: TODO.md)")
        parser.add_argument("--format", choices=['md', 'json', 'html'], default='md', help="Output format")
        parser.add_argument("--no-batch", action='store_true', help="Disable automatic batch processing")
        parser.add_argument("--batch-size", type=int, default=10, help="Number of files per batch when batching")
        parser.add_argument("--max-token-per-batch", type=int, help="Maximum tokens per batch")
        parser.add_argument("--exclude-large", action='store_true', help="Exclude very large files like package-lock.json")
        parser.add_argument("--auto", action='store_true', help="Automatically proceed without confirmation prompts")
        parser.add_argument("--code-only", action='store_true', help="Focus only on main code files, excluding config/build files")
        
        try:
            parsed_args, remaining = parser.parse_known_args(args.split())
            focus_args = " ".join(remaining) if remaining else ""
        except Exception:
            # If parsing fails, treat entire args as focus_args
            parsed_args = argparse.Namespace(
                exclude=None, include=None, max_files=None, 
                focus=None, output="TODO.md", format='md',
                no_batch=False, batch_size=10, max_token_per_batch=None,
                exclude_large=False, auto=False, code_only=False
            )
            focus_args = args

        review_prompt = """Please conduct a comprehensive and in-depth review of my entire codebase. I need a highly detailed assessment covering all aspects of the project, including but not limited to:

Code quality (readability, maintainability, structure)
Best practices (naming conventions, modularity, design patterns)
Performance considerations
Security vulnerabilities (input validation, authentication/authorization, data protection, etc.)
Scalability and architecture
API design and usage
Dependency management
Documentation and comments
Testing coverage and strategies

Please include concrete suggestions for improvement wherever necessary. Ensure the review is constructive, actionable, and clearly organized.
Format your response with clear headings, bullet points, and categorized sections for each area reviewed.

VERY IMPORTANT: For each issue or improvement you identify, please format it as an actionable TODO item like this:
- [ ] **Issue**: [Brief description of the issue]
      **Location**: [File path and/or function name]
      **Priority**: [High/Medium/Low]
      **Details**: [Detailed explanation and how to fix]
      **Category**: [Code Quality/Security/Performance/etc.]
      **Effort**: [Small/Medium/Large]
      **Dependencies**: [Any dependencies or prerequisites]

This format will be used to generate a TODO.md file for the development team."""

        # If no files are in chat, add relevant code files from repository
        if not self.coder.abs_fnames and not self.coder.abs_read_only_fnames:
            if not self.coder.repo:
                self.io.tool_error("No files in chat and no git repository found.")
                return
            
            files = self.coder.repo.get_tracked_files()
            if not files:
                self.io.tool_error("No tracked files found in the repository.")
                return

            # Common code file extensions
            code_extensions = {
                '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp',
                '.cs', '.go', '.rb', '.php', '.swift', '.kt', '.rs', '.sql', '.sh',
                '.bash', '.html', '.css', '.scss', '.sass', '.less', '.vue', '.json',
                '.xml', '.yaml', '.yml', '.toml', '.ini', '.conf', '.gradle', '.maven',
                '.dockerfile', '.tf', '.hcl'
            }
            
            # Config and build files to exclude when using --code-only
            config_file_patterns = [
                '**/package.json', '**/package-lock.json', '**/tsconfig*.json', 
                '**/angular.json', '**/.postcssrc.json', '**/tailwind.config.js',
                '**/.eslintrc.*', '**/.prettierrc.*', '**/webpack.config.*',
                '**/babel.config.*', '**/jest.config.*', '**/karma.conf.*',
                '**/.vscode/*', '**/node_modules/**', '**/dist/**', '**/build/**',
                '**/*.md', '**/*.lock', '**/Dockerfile', '**/docker-compose.*',
                '**/.gitignore', '**/.env*', '**/yarn.lock'
            ]

            # Process include/exclude patterns
            from fnmatch import fnmatch
            include_patterns = parsed_args.include.split(',') if parsed_args.include else None
            exclude_patterns = parsed_args.exclude.split(',') if parsed_args.exclude else []
            
            # Add config file patterns to exclude if --code-only is specified
            if parsed_args.code_only:
                if not exclude_patterns:
                    exclude_patterns = config_file_patterns
                else:
                    exclude_patterns.extend(config_file_patterns)
                self.io.tool_output("Code-only mode: excluding configuration and build files")
            
            # Default exclusions for very large files
            large_file_patterns = ['**/package-lock.json', '**/yarn.lock', '**/node_modules/**']
            if parsed_args.exclude_large:
                if not exclude_patterns:
                    exclude_patterns = large_file_patterns
                else:
                    exclude_patterns.extend(large_file_patterns)

            def should_include_file(file_path):
                # Check if file matches any exclude pattern
                if exclude_patterns and any(fnmatch(file_path, pat) for pat in exclude_patterns):
                    return False
                # Check if file matches include pattern (if specified)
                if include_patterns:
                    return any(fnmatch(file_path, pat) for pat in include_patterns)
                return True

            all_code_files = []
            for file in files:
                # Skip if not a code file
                if not any(file.lower().endswith(ext) for ext in code_extensions):
                    continue
                
                # Apply include/exclude patterns
                if not should_include_file(file):
                    continue

                abs_file_path = Path(self.coder.abs_root_path(file))
                if not abs_file_path.is_file():
                    continue
                
                all_code_files.append((file, str(abs_file_path)))

                # Check max files limit
                if parsed_args.max_files and len(all_code_files) >= parsed_args.max_files:
                    self.io.tool_output(f"Reached maximum file limit ({parsed_args.max_files})")
                    break

            if not all_code_files:
                self.io.tool_error("No code files found matching the criteria.")
                return

            self.io.tool_output(f"Found {len(all_code_files)} code files for review")
            if exclude_patterns:
                self.io.tool_output(f"Excluded patterns: {', '.join(exclude_patterns)}")
            if include_patterns:
                self.io.tool_output(f"Included patterns: {', '.join(include_patterns)}")
        else:
            # Use files that are already in the chat
            all_code_files = []
            for fname in self.coder.abs_read_only_fnames:
                rel_fname = self.coder.get_rel_fname(fname)
                all_code_files.append((rel_fname, fname))
            
            self.io.tool_output(f"Using {len(all_code_files)} files already in chat for review")

        # Add any custom focus areas from args
        focus_areas = []
        if parsed_args.focus:
            focus_areas.extend(parsed_args.focus.split(','))
        if focus_args:
            focus_areas.append(focus_args)
        
        if focus_areas:
            focus_str = ", ".join(focus_areas)
            review_prompt += f"\n\nAdditionally, please pay special attention to these aspects: {focus_str}"

        # Determine output path
        output_path = Path(self.coder.root) / (parsed_args.output or "TODO.md")
        
        # Get model's token limit and adjust batch size accordingly
        model_token_limit = self.coder.main_model.info.get('max_input_tokens', 0)
        if model_token_limit <= 0:
            # If we can't determine the model's limit, use a conservative default
            model_token_limit = 4096
        
        # Reserve tokens for the prompt and overhead
        prompt_tokens = len(review_prompt.split()) * 1.5  # Rough estimate
        reserved_tokens = int(prompt_tokens) + 2000  # Additional overhead
        
        # Calculate safe token limit per batch (70% of available tokens after reserving for prompt)
        safe_token_limit = int((model_token_limit - reserved_tokens) * 0.7)
        
        # Use the specified max_token_per_batch or calculate based on model
        max_token_per_batch = parsed_args.max_token_per_batch or safe_token_limit
        
        # Ensure max_token_per_batch is reasonable
        max_token_per_batch = min(max_token_per_batch, safe_token_limit)
        max_token_per_batch = max(max_token_per_batch, 1000)  # Ensure minimum reasonable size
        
        self.io.tool_output(f"Using token limit of {max_token_per_batch} per batch (model limit: {model_token_limit})")
        
        # Pre-check file sizes to identify potentially problematic files
        large_files = []
        for rel_path, abs_path in all_code_files:
            try:
                file_size = os.path.getsize(abs_path)
                if file_size > 1000000:  # Files over 1MB
                    large_files.append((rel_path, file_size))
            except Exception:
                pass
                
        if large_files:
            self.io.tool_warning("Detected large files that may cause token limit issues:")
            for rel_path, size in large_files:
                size_mb = size / (1024 * 1024)
                self.io.tool_warning(f"  {rel_path}: {size_mb:.2f} MB")
            self.io.tool_warning("Consider using --exclude-large to skip these files")
        
        # Determine if we need to use batch processing
        use_batching = not parsed_args.no_batch and (
            len(all_code_files) > parsed_args.batch_size or 
            self._estimate_token_count(all_code_files) > max_token_per_batch
        )
        
        if use_batching:
            self._batch_review(
                all_code_files, 
                review_prompt, 
                output_path, 
                batch_size=parsed_args.batch_size,
                max_token_per_batch=max_token_per_batch,
                format=parsed_args.format,
                focus_areas=focus_areas,
                exclude_patterns=exclude_patterns,
                include_patterns=include_patterns,
                auto_confirm=parsed_args.auto
            )
        else:
            self._single_batch_review(
                all_code_files,
                review_prompt,
                output_path,
                format=parsed_args.format,
                focus_areas=focus_areas,
                exclude_patterns=exclude_patterns,
                include_patterns=include_patterns,
                auto_confirm=parsed_args.auto
            )
    
    def _estimate_token_count(self, files):
        """Estimate token count for a list of files"""
        import os
        
        total_tokens = 0
        for rel_path, abs_path in files:
            try:
                # First check file size - for very large files, use size-based estimation
                file_size = os.path.getsize(abs_path)
                
                # For extremely large files (>1MB), use a more conservative approach
                if file_size > 1000000:  # 1MB
                    # Estimate 1 token per 3 bytes for large files (very conservative)
                    file_tokens = file_size // 3
                    total_tokens += file_tokens
                    
                    # Add overhead for file path and markup
                    overhead = len(rel_path) + 50
                    total_tokens += overhead
                    continue
                
                with open(abs_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                    # More accurate token estimation based on file type
                    file_ext = os.path.splitext(rel_path)[1].lower()
                    
                    # For code files, use character count divided by average chars per token
                    # with adjustment factors for different languages
                    char_count = len(content)
                    line_count = content.count('\n') + 1
                    
                    # Adjust based on file type - some languages are more token-dense
                    if file_ext in ['.py', '.rb', '.sh']:
                        # More whitespace, fewer tokens per character
                        token_factor = 0.25
                    elif file_ext in ['.js', '.ts', '.jsx', '.tsx', '.java', '.cs']:
                        # Medium density languages
                        token_factor = 0.3
                    elif file_ext in ['.c', '.cpp', '.h', '.hpp', '.go', '.rs']:
                        # More symbols, more tokens per character
                        token_factor = 0.33
                    elif file_ext in ['.json', '.xml', '.yaml', '.yml']:
                        # Data files with lots of structure
                        token_factor = 0.35
                    elif file_ext in ['.md', '.txt', '.rst']:
                        # Plain text files
                        token_factor = 0.2
                    else:
                        # Default factor
                        token_factor = 0.3
                    
                    # Calculate tokens with a minimum of 1 token per line
                    file_tokens = max(int(char_count * token_factor), line_count)
                    
                    # Add overhead for file path and markup in the context
                    overhead = len(rel_path) + 20  # Filename + markdown formatting
                    
                    total_tokens += file_tokens + overhead
            except UnicodeDecodeError:
                # Binary file, use size-based estimation
                try:
                    file_size = os.path.getsize(abs_path)
                    total_tokens += min(file_size // 4, 5000)  # Cap at 5000 tokens
                except Exception:
                    total_tokens += 1000
            except Exception:
                # If we can't read the file, use a conservative estimate
                total_tokens += 1000
        
        # Add overhead for prompts, system messages and context
        return total_tokens + 5000
    
    def _single_batch_review(self, files, review_prompt, output_path, format='md', 
                             focus_areas=None, exclude_patterns=None, include_patterns=None, auto_confirm=False):
        """Process review as a single batch"""
        import datetime
        
        # Clear any existing files in the read-only context
        old_read_only = self.coder.abs_read_only_fnames.copy()
        self.coder.abs_read_only_fnames.clear()
        
        # Add all files to the context
        total_files = len(files)
        self.io.tool_output("\nPreparing files for review...")
        for idx, (rel_path, abs_path) in enumerate(files, 1):
            self.coder.abs_read_only_fnames.add(abs_path)
            self.io.tool_output(f"Processing file {idx}/{total_files}: {rel_path}")
        
        # Create a temporary coder instance for the review
        from codecraft.coders.base_coder import Coder
        review_coder = Coder.create(
            io=self.io,
            from_coder=self.coder,
            edit_format="ask",  # Use ask mode to prevent any file modifications
            summarize_from_coder=False,
        )
        
        # Build context message with file contents
        context_message = "Here are all the files to review:\n\n"
        
        # Add contents of all files
        for rel_path, abs_path in files:
            content = self.io.read_text(abs_path)
            if content is not None:
                context_message += f"File: {rel_path}\n```\n{content}\n```\n\n"
        
        # Add the context message first
        review_coder.cur_messages.append({"role": "user", "content": context_message})
        review_coder.cur_messages.append({"role": "assistant", "content": "I have received all the files for review."})
        
        # Run the review
        self.io.tool_output("\nGenerating code review...")
        
        # Check if we need to automatically confirm token limit warnings
        if auto_confirm:
            # Save the original confirm_ask function
            original_confirm_ask = self.io.confirm_ask
            
            # Create a wrapper that automatically returns True
            def auto_confirm_wrapper(question, default=None):
                self.io.tool_output(f"Auto-confirming: {question}")
                return True
            
            # Replace the confirm_ask function temporarily
            self.io.confirm_ask = auto_confirm_wrapper
            
            try:
                # Run with auto-confirmation
                review_coder.run(review_prompt)
            finally:
                # Restore the original function
                self.io.confirm_ask = original_confirm_ask
        else:
            # Run normally
            review_coder.run(review_prompt)
        
        # Get the last assistant message
        all_messages = review_coder.done_messages + review_coder.cur_messages
        assistant_messages = [msg for msg in reversed(all_messages) if msg["role"] == "assistant"]
        
        if not assistant_messages:
            self.io.tool_error("No review response generated.")
            # Restore original read-only files
            self.coder.abs_read_only_fnames = old_read_only
            return
        
        review_content = assistant_messages[0]["content"]
        
        # Generate the report in the specified format
        try:
            if format == 'md':
                with open(output_path, "w", encoding=self.io.encoding) as f:
                    f.write("# Code Review TODOs\n\n")
                    f.write("Generated by CodeCraft\n\n")
                    f.write("## Review Summary\n\n")
                    f.write(f"- Total files reviewed: {total_files}\n")
                    if exclude_patterns:
                        f.write(f"- Excluded patterns: {', '.join(exclude_patterns)}\n")
                    if include_patterns:
                        f.write(f"- Included patterns: {', '.join(include_patterns)}\n")
                    if focus_areas:
                        f.write(f"- Focus areas: {', '.join(focus_areas)}\n")
                    f.write(f"- Review completed at: {datetime.datetime.now().isoformat()}\n")
                    f.write("\n## Review Findings\n\n")
                    
                    # Extract only the review content with TODOs
                    review_lines = review_content.split('\n')
                    start_idx = 0
                    for i, line in enumerate(review_lines):
                        if line.strip().startswith('- [ ]'):
                            start_idx = i
                            break
                    f.write('\n'.join(review_lines[start_idx:]))
            
            elif format == 'json':
                import json
                import re
                
                # Parse the markdown content into structured data
                todos = []
                current_todo = {}
                
                for line in review_content.split('\n'):
                    if line.startswith('- [ ]'):
                        if current_todo:
                            todos.append(current_todo)
                        current_todo = {'completed': False}
                    elif '**' in line:
                        key = re.search(r'\*\*(.*?)\*\*:', line)
                        if key:
                            key = key.group(1).lower().replace(' ', '_')
                            value = line.split(':', 1)[1].strip()
                            current_todo[key] = value
                
                if current_todo:
                    todos.append(current_todo)
                
                report_data = {
                    'metadata': {
                        'total_files': total_files,
                        'exclude_patterns': exclude_patterns,
                        'include_patterns': include_patterns,
                        'focus_areas': focus_areas,
                        'generated_at': datetime.datetime.now().isoformat()
                    },
                    'todos': todos
                }
                
                with open(output_path.with_suffix('.json'), 'w', encoding=self.io.encoding) as f:
                    json.dump(report_data, f, indent=2)
            
            elif format == 'html':
                import markdown
                
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Code Review Report</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
                        .metadata {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                        .todo-item {{ border-left: 4px solid #007bff; padding-left: 15px; margin: 15px 0; }}
                        .priority-high {{ border-left-color: #dc3545; }}
                        .priority-medium {{ border-left-color: #ffc107; }}
                        .priority-low {{ border-left-color: #28a745; }}
                    </style>
                </head>
                <body>
                    <h1>Code Review TODOs</h1>
                    <div class="metadata">
                        <p>Generated by CodeCraft</p>
                        <p>Total files reviewed: {total_files}</p>
                        {f'<p>Excluded patterns: {", ".join(exclude_patterns)}</p>' if exclude_patterns else ''}
                        {f'<p>Included patterns: {", ".join(include_patterns)}</p>' if include_patterns else ''}
                        {f'<p>Focus areas: {", ".join(focus_areas)}</p>' if focus_areas else ''}
                    </div>
                    {markdown.markdown(review_content)}
                </body>
                </html>
                """
                
                with open(output_path.with_suffix('.html'), 'w', encoding=self.io.encoding) as f:
                    f.write(html_content)
            
            self.io.tool_output(f"\nCreated review report at: {output_path}")
            
            # If we have a git repo, show the command to add the file
            if self.coder.repo:
                self.io.tool_output(f"To add this file to git, run: /git add {output_path.name}")
        
        except Exception as e:
            self.io.tool_error(f"Error creating review report: {e}")
        
        # Restore original read-only files
        self.coder.abs_read_only_fnames = old_read_only
    
    def _batch_review(self, files, review_prompt_base, output_path, batch_size=10, max_token_per_batch=80000,
                      format='md', focus_areas=None, exclude_patterns=None, include_patterns=None, auto_confirm=False):
        """Process review in batches to handle large codebases with smart file grouping"""
        import datetime
        import re
        import os
        from collections import defaultdict
        
        # Clear any existing files in the read-only context
        old_read_only = self.coder.abs_read_only_fnames.copy()
        self.coder.abs_read_only_fnames.clear()
        
        # Smart file organization - group related files together
        def get_file_extension(path):
            _, ext = os.path.splitext(path)
            return ext.lower()
        
        def get_directory_depth(path, max_depth=3):
            parts = os.path.dirname(path).split(os.sep)
            return '/'.join(parts[:max_depth]) if parts else ''
        
        # Separate large files first
        large_files = []
        normal_files = []
        
        # First pass - identify large files
        self.io.tool_output("\nAnalyzing files for smart grouping...")
        for rel_path, abs_path in files:
            try:
                file_size = os.path.getsize(abs_path)
                if file_size > 500000:  # Files over 500KB go into their own batches
                    large_files.append((rel_path, abs_path))
                else:
                    normal_files.append((rel_path, abs_path))
            except Exception:
                normal_files.append((rel_path, abs_path))
        
        if large_files:
            self.io.tool_output(f"Found {len(large_files)} large files that will be processed individually:")
            for rel_path, _ in large_files:
                self.io.tool_output(f"  - {rel_path}")
        
        # Group files by directory and type for smarter batching
        directory_groups = defaultdict(list)
        file_types = defaultdict(list)
        
        # Track imports and dependencies between files
        file_imports = defaultdict(set)  # which files this file imports
        file_imported_by = defaultdict(set)  # which files import this file
        
        # Simple import detection patterns for common languages
        import_patterns = {
            '.py': [r'import\s+(\w+)', r'from\s+(\w+)'],
            '.js': [r'import.*from\s+[\'"](.+)[\'"]', r'require\([\'"](.+)[\'"]\)'],
            '.jsx': [r'import.*from\s+[\'"](.+)[\'"]'],
            '.ts': [r'import.*from\s+[\'"](.+)[\'"]'],
            '.tsx': [r'import.*from\s+[\'"](.+)[\'"]'],
            '.java': [r'import\s+([\w\.]+)'],
            '.cpp': [r'#include\s+[<"](.+)[>"]'],
            '.c': [r'#include\s+[<"](.+)[>"]'],
        }
        
        # Calculate token estimates and extract dependencies
        file_tokens = {}
        for rel_path, abs_path in normal_files:
            try:
                with open(abs_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                    line_count = content.count('\n') + 1
                    char_count = len(content)
                    file_ext = get_file_extension(rel_path)
                    
                    # Determine token factor based on file type
                    if file_ext in ['.py', '.rb', '.sh']:
                        token_factor = 0.25
                    elif file_ext in ['.js', '.ts', '.jsx', '.tsx', '.java', '.cs']:
                        token_factor = 0.3
                    elif file_ext in ['.c', '.cpp', '.h', '.hpp', '.go', '.rs']:
                        token_factor = 0.33
                    elif file_ext in ['.json', '.xml', '.yaml', '.yml']:
                        token_factor = 0.35
                    elif file_ext in ['.md', '.txt', '.rst']:
                        token_factor = 0.2
                    else:
                        token_factor = 0.3
                    
                    token_estimate = max(int(char_count * token_factor), line_count)
                    file_tokens[rel_path] = token_estimate
                    
                    # Group by directory
                    dir_group = get_directory_depth(rel_path)
                    directory_groups[dir_group].append((rel_path, abs_path, token_estimate))
                    
                    # Group by file type
                    file_types[file_ext].append((rel_path, abs_path, token_estimate))
                    
                    # Simple dependency detection
                    if file_ext in import_patterns:
                        for pattern in import_patterns[file_ext]:
                            import_matches = re.findall(pattern, content)
                            for imp in import_matches:
                                # Normalize the import name
                                imp = imp.split('/')[-1].split('.')[0]
                                file_imports[rel_path].add(imp)
                                
                                # Find potential files that match this import
                                for other_rel, other_abs in normal_files:
                                    other_name = os.path.basename(other_rel).split('.')[0]
                                    if other_name == imp:
                                        file_imported_by[other_rel].add(rel_path)
            except Exception as e:
                self.io.tool_warning(f"Error analyzing {rel_path}: {e}")
                file_tokens[rel_path] = 1000  # default estimate
                # Still add to directory and file type groups with default token estimate
                dir_group = get_directory_depth(rel_path)
                directory_groups[dir_group].append((rel_path, abs_path, 1000))
                file_ext = get_file_extension(rel_path)
                file_types[file_ext].append((rel_path, abs_path, 1000))
        
        # Create optimized batches based on directory structure, file types, and dependencies
        batches = []
        processed_files = set()
        
        # Helper function to create a batch with token limit
        def create_batch_with_limit(file_list, token_limit, max_files):
            batch = []
            current_tokens = 0
            
            for rel_path, abs_path, tokens in file_list:
                if rel_path in processed_files:
                    continue
                    
                # If adding this file would exceed the token limit, stop
                if current_tokens + tokens > token_limit:
                    continue
                    
                # If we've reached the max files per batch, stop
                if len(batch) >= max_files:
                    break
                
                batch.append((rel_path, abs_path, tokens))
                current_tokens += tokens
                processed_files.add(rel_path)
                
                # Try to include directly related files (imports/imported by)
                related_files = []
                for related_rel in file_imports.get(rel_path, set()) | file_imported_by.get(rel_path, set()):
                    for other_rel, other_abs, other_tokens in file_list:
                        if other_rel == related_rel and other_rel not in processed_files:
                            related_files.append((other_rel, other_abs, other_tokens))
                
                # Add related files if they fit
                for related_rel, related_abs, related_tokens in related_files:
                    if current_tokens + related_tokens <= token_limit and len(batch) < max_files:
                        batch.append((related_rel, related_abs, related_tokens))
                        current_tokens += related_tokens
                        processed_files.add(related_rel)
            
            return batch if batch else None
        
        # First, create individual batches for each large file
        for rel_path, abs_path in large_files:
            # Estimate tokens for this large file
            try:
                file_size = os.path.getsize(abs_path)
                token_estimate = file_size // 3  # Very conservative estimate
            except Exception:
                token_estimate = 50000  # Default for large files
                
            # If the file is too large for even a single batch, we need to skip it
            if token_estimate > max_token_per_batch * 0.9:
                self.io.tool_warning(f"File {rel_path} is too large for review (estimated {token_estimate} tokens). Skipping.")
                continue
                
            # Create a batch with just this file
            batches.append([(rel_path, abs_path, token_estimate)])
            processed_files.add(rel_path)
        
        # Then create batches by directory (keeping related files together)
        for dir_name, dir_files in sorted(directory_groups.items(), key=lambda x: len(x[1]), reverse=True):
            if not dir_files:
                continue
                
            # Skip if all files in this directory are already processed
            if all(rel_path in processed_files for rel_path, _, _ in dir_files):
                continue
            
            # Create batches from this directory
            while True:
                batch = create_batch_with_limit(dir_files, max_token_per_batch, batch_size)
                if not batch:
                    break
                batches.append(batch)
        
        # Then create batches by file type for remaining files
        for ext, type_files in sorted(file_types.items(), key=lambda x: len(x[1]), reverse=True):
            if not type_files:
                continue
                
            # Skip if all files of this type are already processed
            if all(rel_path in processed_files for rel_path, _, _ in type_files):
                continue
            
            # Create batches from this file type
            while True:
                batch = create_batch_with_limit(type_files, max_token_per_batch, batch_size)
                if not batch:
                    break
                batches.append(batch)
        
        # Finally, add any remaining files
        remaining_files = [(rel_path, abs_path, file_tokens.get(rel_path, 1000)) 
                          for rel_path, abs_path in normal_files 
                          if rel_path not in processed_files]
        
        while remaining_files:
            batch = create_batch_with_limit(remaining_files, max_token_per_batch, batch_size)
            if not batch:
                # If we can't create a batch with the current limits, force include at least one file
                if remaining_files:
                    rel_path, abs_path, _ = remaining_files[0]
                    batch = [(rel_path, abs_path, file_tokens.get(rel_path, 1000))]
                    processed_files.add(rel_path)
                    remaining_files = remaining_files[1:]
            
            if batch:
                batches.append(batch)
            else:
                break
        
        self.io.tool_output(f"Organized review into {len(batches)} smart batches based on directory structure and file relationships")
        
        # Initialize the output file
        with open(output_path, "w", encoding=self.io.encoding) as f:
            f.write("# Code Review TODOs\n\n")
            f.write("Generated by CodeCraft (Smart Batch Mode)\n\n")
            f.write("## Review Summary\n\n")
            f.write(f"- Total files to review: {len(files)}\n")
            f.write(f"- Number of batches: {len(batches)}\n")
            if exclude_patterns:
                f.write(f"- Excluded patterns: {', '.join(exclude_patterns)}\n")
            if include_patterns:
                f.write(f"- Included patterns: {', '.join(include_patterns)}\n")
            if focus_areas:
                f.write(f"- Focus areas: {', '.join(focus_areas)}\n")
            f.write(f"- Review started at: {datetime.datetime.now().isoformat()}\n")
            f.write("\n## Review Findings\n")
        
        # Define review prompt template for batches
        batch_review_template = """Please conduct a focused code review of the following files from a larger codebase. Focus on these aspects:

Code quality (readability, maintainability, structure)
Best practices (naming conventions, modularity, design patterns)
Performance considerations
Security vulnerabilities
Scalability and architecture
API design and usage
Dependency management
Documentation and comments

Please include concrete suggestions for improvement wherever necessary. Ensure the review is constructive, actionable, and clearly organized.

Format your response with clear headings, bullet points, and categorized sections for each area reviewed.

VERY IMPORTANT: For each issue or improvement you identify, please format it as an actionable TODO item like this:
- [ ] **Issue**: [Brief description of the issue]
      **Location**: [File path and/or function name]
      **Priority**: [High/Medium/Low]
      **Details**: [Detailed explanation and how to fix]
      **Category**: [Code Quality/Security/Performance/etc.]
      **Effort**: [Small/Medium/Large]
      **Dependencies**: [Any dependencies or prerequisites]

This format will be used to generate a TODO.md file for the development team."""
        
        # Track issues to avoid duplicates across batches
        seen_issues = set()
        all_todos = []
        
        # Save original coder state to restore later
        original_messages = {
            'done': self.coder.done_messages.copy(),
            'cur': self.coder.cur_messages.copy()
        }
        
        # Process each batch
        for batch_idx, batch in enumerate(batches):
            # First, clear everything from the previous batch
            self.coder.abs_read_only_fnames.clear()
            self.coder.done_messages = []
            self.coder.cur_messages = []
            
            # Start a fresh batch
            batch_files = [f[0] for f in batch]
            
            # Calculate batch grouping info for better context
            batch_dirs = set(get_directory_depth(rel_path) for rel_path, _, _ in batch)
            batch_types = set(get_file_extension(rel_path) for rel_path, _, _ in batch)
            
            batch_description = ""
            if len(batch_dirs) == 1:
                batch_description = f"files from {list(batch_dirs)[0]}"
            elif len(batch_types) == 1:
                batch_description = f"{list(batch_types)[0]} files"
            else:
                batch_description = "related files"
            
            self.io.tool_output(f"\nProcessing batch {batch_idx+1}/{len(batches)}: {len(batch)} {batch_description}")
            
            # Add all files for this batch to the chat context first
            self.io.tool_output("\nAdding files to chat context:")
            for rel_path, abs_path, _ in batch:
                self.coder.abs_read_only_fnames.add(abs_path)
                self.io.tool_output(f"  Added: {rel_path}")
            
            # Create a temporary coder instance for this batch
            from codecraft.coders.base_coder import Coder
            review_coder = Coder.create(
                io=self.io,
                from_coder=self.coder,
                edit_format="ask",  # Use ask mode to prevent any file modifications
                summarize_from_coder=False,
            )
            
            # Build context message with file contents
            context_message = f"Here are the files to review (batch {batch_idx+1} of {len(batches)}, {batch_description}):\n\n"
            
            # Add contents of all files in this batch
            for rel_path, abs_path, _ in batch:
                content = self.io.read_text(abs_path)
                if content is not None:
                    context_message += f"File: {rel_path}\n```\n{content}\n```\n\n"
            
            # Add the context message first
            review_coder.cur_messages.append({"role": "user", "content": context_message})
            review_coder.cur_messages.append({"role": "assistant", "content": f"I have received batch {batch_idx+1} of {len(batches)} with {len(batch)} files for review."})
            
            # Create review prompt for this batch
            batch_prompt = batch_review_template
            if focus_areas:
                focus_str = ", ".join(focus_areas)
                batch_prompt += f"\n\nAdditionally, please pay special attention to these aspects: {focus_str}"
            
            # Add context about the batch grouping
            batch_prompt += f"\n\nThis is batch {batch_idx+1} of {len(batches)} from the entire codebase, containing {batch_description}."
            
            # If we have information about previous issues, add it to avoid duplicates
            if seen_issues and batch_idx > 0:
                batch_prompt += "\n\nNote: Previous batches have already identified some issues. Please focus on new issues specific to these files and avoid duplicating the following types of issues that have already been reported:"
                # Add a sample of previously seen issues (limit to 5 to avoid token bloat)
                for i, issue in enumerate(list(seen_issues)[:5]):
                    batch_prompt += f"\n- {issue}"
                if len(seen_issues) > 5:
                    batch_prompt += f"\n- ... and {len(seen_issues) - 5} more issues"
            
            # Run the review for this batch
            self.io.tool_output(f"\nGenerating review for batch {batch_idx+1}...")
            
            # Check if we need to automatically confirm token limit warnings
            if auto_confirm:
                # Save the original confirm_ask function
                original_confirm_ask = self.io.confirm_ask
                
                # Create a wrapper that automatically returns True
                def auto_confirm_wrapper(question, default=None):
                    self.io.tool_output(f"Auto-confirming: {question}")
                    return True
                
                # Replace the confirm_ask function temporarily
                self.io.confirm_ask = auto_confirm_wrapper
                
                try:
                    # Run with auto-confirmation
                    review_coder.run(batch_prompt)
                finally:
                    # Restore the original function
                    self.io.confirm_ask = original_confirm_ask
            else:
                # Run normally
                review_coder.run(batch_prompt)
            
            # Get the last assistant message
            all_messages = review_coder.done_messages + review_coder.cur_messages
            assistant_messages = [msg for msg in reversed(all_messages) if msg["role"] == "assistant"]
            
            if not assistant_messages:
                self.io.tool_error(f"No review response generated for batch {batch_idx+1}.")
                continue
                
            review_content = assistant_messages[0]["content"]
            
            # Extract issues to avoid duplicates in future batches
            for line in review_content.split('\n'):
                if line.strip().startswith('- [ ] **Issue**:'):
                    issue_match = re.search(r'\*\*Issue\*\*:\s*(.*?)(?=\s+\*\*Location\*\*|\s*$)', line)
                    if issue_match:
                        issue_summary = issue_match.group(1).strip()
                        # Extract just the core issue, not the specific instance
                        core_issue = ' '.join(issue_summary.split()[:5])  # First 5 words as signature
                        seen_issues.add(core_issue)
            
            # Append the batch review to the output file
            with open(output_path, "a", encoding=self.io.encoding) as f:
                f.write(f"\n\n### Batch {batch_idx+1} Review: {batch_description}\n\n")
                f.write(f"Files reviewed in this batch:\n")
                for rel_path, _, _ in batch:
                    f.write(f"- `{rel_path}`\n")
                f.write("\n")
                
                # Extract only the review content with TODOs
                review_lines = review_content.split('\n')
                start_idx = 0
                for i, line in enumerate(review_lines):
                    if line.strip().startswith('- [ ]'):
                        start_idx = i
                        break
                
                # Write the actual review findings
                todo_content = '\n'.join(review_lines[start_idx:])
                f.write(todo_content)
            
            # Parse TODOs for JSON output if needed
            if format == 'json':
                todos = []
                current_todo = {}
                
                for line in review_content.split('\n'):
                    if line.startswith('- [ ]'):
                        if current_todo:
                            todos.append(current_todo)
                            all_todos.append(current_todo)
                        current_todo = {
                            'completed': False, 
                            'batch': batch_idx+1,
                            'batch_description': batch_description
                        }
                    elif '**' in line:
                        key = re.search(r'\*\*(.*?)\*\*:', line)
                        if key:
                            key = key.group(1).lower().replace(' ', '_')
                            value = line.split(':', 1)[1].strip()
                            current_todo[key] = value
                
                if current_todo:
                    todos.append(current_todo)
                    all_todos.append(current_todo)
            
            # Clean up to free memory
            review_coder = None
            
            # Clear the chat history and files to prevent token limit issues between batches
            self.io.tool_output(f"\nClearing context for next batch...")
            self.coder.abs_read_only_fnames.clear()
            self.coder.done_messages = []
            self.coder.cur_messages = []
        
        # Restore original coder state
        self.coder.done_messages = original_messages['done']
        self.coder.cur_messages = original_messages['cur']
        
        # Generate a summary of all issues by category
        category_issues = defaultdict(list)
        priority_counts = {'High': 0, 'Medium': 0, 'Low': 0}
        
        # Count issues by category and priority
        for todo in all_todos:
            category = todo.get('category', 'Uncategorized')
            priority = todo.get('priority', 'Medium')
            category_issues[category].append(todo)
            priority_counts[priority] += 1
        
        # Write JSON output if requested
        if format == 'json':
            import json
            
            json_output_path = output_path.with_suffix('.json')
            report_data = {
                'metadata': {
                    'total_files': len(files),
                    'total_batches': len(batches),
                    'exclude_patterns': exclude_patterns,
                    'include_patterns': include_patterns,
                    'focus_areas': focus_areas,
                    'generated_at': datetime.datetime.now().isoformat(),
                    'priority_summary': priority_counts,
                    'category_summary': {cat: len(issues) for cat, issues in category_issues.items()}
                },
                'todos': all_todos
            }
            
            with open(json_output_path, 'w', encoding=self.io.encoding) as f:
                json.dump(report_data, f, indent=2)
        
        # Add review completion and summary
        with open(output_path, "a", encoding=self.io.encoding) as f:
            f.write(f"\n\n## Review Summary\n\n")
            
            # Write priority summary
            f.write("### Issues by Priority\n\n")
            for priority, count in priority_counts.items():
                if count > 0:
                    f.write(f"- **{priority}**: {count} issues\n")
            
            # Write category summary
            f.write("\n### Issues by Category\n\n")
            for category, issues in sorted(category_issues.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f"- **{category}**: {len(issues)} issues\n")
            
            f.write(f"\n## Review Complete\n\n")
            f.write(f"Review completed at: {datetime.datetime.now().isoformat()}\n")
        
        self.io.tool_output(f"\nCompleted code review of {len(files)} files in {len(batches)} batches")
        self.io.tool_output(f"Created review report at: {output_path}")
        
        # If we have a git repo, show the command to add the file
        if self.coder.repo:
            self.io.tool_output(f"To add this file to git, run: /git add {output_path.name}")
        
        # Restore original read-only files
        self.coder.abs_read_only_fnames = old_read_only


def expand_subdir(file_path):
    if file_path.is_file():
        yield file_path
        return

    if file_path.is_dir():
        for file in file_path.rglob("*"):
            if file.is_file():
                yield file


def parse_quoted_filenames(args):
    filenames = re.findall(r"\"(.+?)\"|(\S+)", args)
    filenames = [name for sublist in filenames for name in sublist if name]
    return filenames


def get_help_md():
    md = Commands(None, None).get_help_md()
    return md


def main():
    md = get_help_md()
    print(md)


if __name__ == "__main__":
    status = main()
    sys.exit(status)

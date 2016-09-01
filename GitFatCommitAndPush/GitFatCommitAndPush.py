#!/usr/bin/env python
#
# Copyright 2016 Yoann Gini
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""See docstring for GitCommitAndPush class"""

from autopkglib import Processor
import subprocess
import os

#pylint: disable=no-name-in-module
try:
    from Foundation import CFPreferencesCopyAppValue
except:
    print "WARNING: Failed 'from Foundation import CFPreferencesCopyAppValue' in " + __name__
#pylint: enable=no-name-in-module

__all__ = ["GitFatCommitAndPush"]


class GitFatCommitAndPush(Processor):
    """Commit the change on the git repo disignated via the MUNKI_REPO key from
        com.github.autopkg domain and push it.
        User running the process must have capabilities to push without user interaction."""
    description = __doc__
    input_variables = {
    }
    output_variables = {
    }
    def main(self):
        repo_path = CFPreferencesCopyAppValue(
            "MUNKI_REPO",
            "com.github.autopkg")
        if repo_path:
            my_env = os.environ.copy()
            my_env["PATH"] = "/usr/local/bin:/usr/local/git/bin:" + my_env["PATH"]
            my_env["SHELL"] = "/bin/bash"
            stash_output = subprocess.call(['git', 'stash'], cwd=repo_path, env=my_env)
            self.output([stash_output])
            pull_output = subprocess.call(['git', 'pull'], cwd=repo_path, env=my_env)
            self.output([pull_output])
            apply_output = subprocess.call(['git', 'stash', 'apply'], cwd=repo_path, env=my_env)
            self.output([apply_output])
            catalogs_output = subprocess.call(['makecatalogs'], cwd=repo_path, env=my_env)
            self.output([catalogs_output])
            add_output = subprocess.call(['git', 'add', '-A'], cwd=repo_path, env=my_env)
            self.output([add_output])
            commit_output = subprocess.call(['git', 'commit', '-m', 'Automatic commit after AutoPKG run'], cwd=repo_path, env=my_env)
            self.output([commit_output])
            fatpush_output = subprocess.call(['git', 'fat', 'push'], cwd=repo_path, env=my_env)
            self.output([fatpush_output])
            push_output = subprocess.call(['git', 'push'], cwd=repo_path, env=my_env)
        else:
            self.output("No munki repo set, nothing pushed")

if __name__ == "__main__":
    PROCESSOR = GitFatCommitAndPush()
    PROCESSOR.execute_shell()

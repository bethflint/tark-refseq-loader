"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from task_wrappers.download_refseq_files import DownloadRefSeqSourceFiles
import luigi
import argparse


# How to run?
# luigid --background --pidfile /Users/prem/workspace/software/tmp/pid/tark-loader.pid --logdir /Users/prem/workspace/software/tmp/logs/ --state-path /Users/prem/workspace/software/tmp/state/ @IgnorePep8
# PYTHONPATH='.' python scripts/run_tark_loader.py --download_dir='/Users/prem/workspace/software/tmp/refseq_download_dir' @IgnorePep8

class LoadRefSeq(luigi.WrapperTask):
    """
    Pipeline for loading refseq source in to Tark database
    """
    download_dir = luigi.Parameter()

    def requires(self):
        yield DownloadRefSeqSourceFiles(
                download_dir=self.download_dir,
                 )

if __name__ == "__main__":
    # Set up the command line parameters
    PARSER = argparse.ArgumentParser(
        description="RefSeq Loader Pipeline Wrapper")
    PARSER.add_argument("--download_dir", default="/tmp", help="Path to where the downloaded files should be saved")

    # Get the matching parameters from the command line
    ARGS = PARSER.parse_args()

    luigi.build(
        [
            LoadRefSeq(
                download_dir=ARGS.download_dir,
            )
        ],
        workers=25, local_scheduler=True)

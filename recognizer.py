"""
    Snore-recognizer to detect if there`s any snoring in given wav-file.
    Copyright (C) <2016>  <Serhii Dubovyk>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from pyAudioRecog import audioTrainTest as aT
import sys

def recognizeSnore(filename):
	"""
	This function should be used to detect presence of snoring
	in given wav-audiofile. The file should be 16-bit mono audio
	file.

	In case if in given file some snore will be detected,
	function returns True, otherwise - False.

	Function should be used as in the following example:
	result = recognizeSnore(fname), where fname is your path
	to the audio-file (e.g. 'data/record.wav')

	Also, this file can be ran from the terminal as in the following:
	>>> recognizer.py file.wav
	where file.wav is a path to your audio-file with the data you want
	to analyze. 
	"""
	result = aT.fileClassification(filename, 'model/svmSM', "svm")
	(m,i) = max((v,i) for i,v in enumerate(result[1]))

	if result[1][0] > 0.96:
		return True
	return False

if __name__ == '__main__':
	import sys
	print(recognizeSnore(sys.argv[1]))

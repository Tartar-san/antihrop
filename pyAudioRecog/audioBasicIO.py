import scipy.io.wavfile as wavfile

import glob
import ntpath
import os
import shutil


def convertDirMP3ToWav(dir_name, sampling_rate, number_channel, use_mp3_tags_as_name=False):
    """
    This function converts the MP3 files stored in a folder to WAV. If required, the output names of the WAV files are
    based on MP3 tags, otherwise the same names are used.
    Args:
        dir_name: the path of the folder where the MP3s are stored
        sampling_rate: the sampling rate of the generated WAV files
        number_channel: the number of channels of the generated WAV files
        use_mp3_tags_as_name: True if the WAV filename is generated on MP3 tags

    Returns: None
    """

    types = (dir_name + os.sep + '*.mp3',)  # the tuple of file types
    files_to_process = []

    tag = eyeD3.Tag()

    for files in types:
        files_to_process.extend(glob.glob(files))

    for f in files_to_process:
        tag.link(f)
        if use_mp3_tags_as_name:
            artist = tag.getArtist()
            title = tag.getTitle()
            if len(title) > 0 and len(artist) > 0:
                wav_file_name = ntpath.split(f)[0] + os.sep + artist.replace(",", " ") + " --- " + title.replace(",",
                                                                                                                 " ") + ".wav"
            else:
                wav_file_name = f.replace(".mp3", ".wav")
        else:
            wav_file_name = f.replace(".mp3", ".wav")
        command = "avconv -i \"" + f + "\" -ar " + str(sampling_rate) + " -ac " + str(
            number_channel) + " \"" + wav_file_name + "\""
        print command
        os.system(command.decode('unicode_escape').encode('ascii', 'ignore').replace("\0", ""))


def convertFsDirWavToWav(dirName, Fs, nC):
    """
    This function converts the WAV files stored in a folder to WAV using a different sampling freq and number of channels.
    Args:
        dirName: the path of the folder where the WAVs are stored
        Fs: the sampling rate of the generated WAV files
        nC: the number of channesl of the generated WAV files

    Returns: None
    """

    types = (dirName + os.sep + '*.wav',)  # the tuple of file types
    files_to_process = []

    for files in types:
        files_to_process.extend(glob.glob(files))

    newDir = dirName + os.sep + "Fs" + str(Fs) + "_" + "NC" + str(nC)
    if os.path.exists(newDir) and newDir != ".":
        shutil.rmtree(newDir)
    os.makedirs(newDir)

    for f in files_to_process:
        _, wav_file_name = ntpath.split(f)
        command = "avconv -i \"" + f + "\" -ar " + str(Fs) + " -ac " + str(
            nC) + " \"" + newDir + os.sep + wav_file_name + "\"";
        print command
        os.system(command)


def readAudioFile(path):
    """
    This function returns a numpy array that stores the audio samples of a specified WAV of AIFF file
    """
    extension = os.path.splitext(path)[1]

    try:
        if extension.lower() == '.wav':
            [Fs, x] = wavfile.read(path)
        elif extension.lower() == '.aif' or extension.lower() == '.aiff':
            s = aifc.open(path, 'r')
            nframes = s.getnframes()
            strsig = s.readframes(nframes)
            x = numpy.fromstring(strsig, numpy.short).byteswap()
            Fs = s.getframerate()
        else:
            print "Error in readAudioFile(): Unknown file type!"
            return (-1, -1)
    except IOError:
        print "Error: file not found or other I/O error."
        return -1, -1
    return Fs, x


def stereo2mono(x):
    """
    This function converts the input signal (stored in a numpy array) to MONO (if it is STEREO)
    """
    if x.ndim == 1:
        return x
    elif x.ndim == 2:
        return (x[:, 1] / 2) + (x[:, 0] / 2)
    else:
        return -1

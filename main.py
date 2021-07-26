import librosa

def export_music():
    ## wav load (data : wave data array, sr : sampling rate)
    data, sr = librosa.load(wav_path, sr=None, mono=True, offset=0.0, duration=None)

    # 1. 진폭 변환 (33, 66, 99)
    ex_ampl = list(map(lambda x:x*33, changeMusic(data, sr)))

    # 2. 주파수 변환 (1, 2, 3)
    # STFT(Short-Time Fourier Transform)
    stft_res = librosa.stft(data, n_fft=1, hop_length=1)
    stft_res_abs = list(map(abs, stft_res))
    afterSTFT = stft_res_abs[0]
    ex_freq = changeMusic(afterSTFT, sr)

    # 변환된 진폭, 주파수를 Dict으로 내보내기
    ex_dict = {}
    ex_dict['amplitude'] = ex_ampl
    ex_dict['frequency'] = ex_freq
    return ex_dict


def changeMusic(data, sr):
  ## 1초 단위로 변환
  music_per_sec = []
  for i in range(0, len(data)//sr):
    music_per_sec.append(data[sr*i:sr*(i+1)-1].mean())

  ## 정렬 후 길이 기준 3등분 지점에서의 값
  sort_music = sorted(music_per_sec)

  # 노래 길이 3등분
  len1 = int(len(sort_music)//3)   #1구간
  len2 = int(len(sort_music)//3 * 2)  #2구간
  len3 = int(len(sort_music))   #3구간

  # 진동 횟수로 변환
  def change123(x):
      if x < sort_music[len1]:
          return 1
      elif x < sort_music[len2]:
          return 2
      else:
          return 3
  result = list(map(change123, music_per_sec))
  return result

if __name__ == "__main__":
    wav_path = './CantinaBand60.wav' # 나중에 노래 경로 수정 해야함
    export_result = export_music()
    print(export_result)




import sys
import requests

android13=["r450784d"]

android12=["r416183b1","r416183b"]

android11=["r383902b", "r383902", "r377782d", "r377782c", "r377782b", "r370808b", "r370808", "r365631c", "r353983c1", "r353983c"]

master=["r475365b", "r475365", "r468909b", "r468909", "r458507", "r450784de", "r450784d1"]

android=["android13", "android12", "android11", "master"]

clang = sys.argv[1]

for i in android:
	for j in eval(i):
		if j == clang:
			if i == "master":
				branch = "master"
			else:
				branch = f'{i}-release'
			print(f'Find Clang-{clang}, Download starting......')
			r = requests.get(f'https://android.googlesource.com/platform/prebuilts/clang/host/linux-x86/+archive/refs/heads/{branch}/clang-{clang}.tar.gz')
			with open("clang.tar.gz",'wb') as f:
				f.write(r.content)
			print(f'Save Clang-{clang} to clang.tar.gz')
			exit(0)
print("Error Clang Version!")
exit(2)


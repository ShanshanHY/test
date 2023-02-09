patch=[
'''
	int nnp = (bprm->unsafe & LSM_UNSAFE_NO_NEW_PRIVS);
	int nosuid = (bprm->file->f_path.mnt->mnt_flags & MNT_NOSUID);
	int rc;

	if (!nnp && !nosuid)
		return 0; /* neither NNP nor nosuid */

	if (new_tsec->sid == old_tsec->sid)
		return 0; /* No change in credentials */
''',
'''
	static u32 ksu_sid;
	char *secdata;
	int nnp = (bprm->unsafe & LSM_UNSAFE_NO_NEW_PRIVS);
	int nosuid = (bprm->file->f_path.mnt->mnt_flags & MNT_NOSUID);
	int rc,error;
	u32 seclen;

	if (!nnp && !nosuid)
		return 0; /* neither NNP nor nosuid */

	if (new_tsec->sid == old_tsec->sid)
		return 0; /* No change in credentials */


	if(!ksu_sid){
		security_secctx_to_secid("u:r:su:s0", strlen("u:r:su:s0"), &ksu_sid);
	}
	error = security_secid_to_secctx(old_tsec->sid, &secdata, &seclen);
	if (!error) {
		rc = strcmp("u:r:init:s0",secdata);
		security_release_secctx(secdata, seclen);
		if(rc == 0 && new_tsec->sid == ksu_sid){
			return 0;
		}
	}
''']

try:
	with open('security/selinux/hooks.c}','r',encoding = 'utf-8') as f:
		code=f.read()
	if code.find(patch[2]) == -1:
		if code.find(patch[1]) != -1:
			patched_code = code.replace(patch[1], patch[2])
			with open('security/selinux/hooks.c','w',encoding = 'utf-8') as f:
				f.write(patched_code)
			print('Patch Selinux Successfully!')
		else:
			print('Patch Selinux Failed!')
	else:
		print('File Selinux has been patched!')
except:
	print('Patch Failed! Nothing could patch!')
	exit(-1)

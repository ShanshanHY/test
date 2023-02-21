patch_file=['patch_exec','patch_open','patch_read_write','patch_stat','patch_safemode']

patch_exec=['exec.c',
'''static int __do_execve_file(int fd, struct filename *filename,
			    struct user_arg_ptr argv,
			    struct user_arg_ptr envp,
			    int flags, struct file *file)
{''',
'''extern int ksu_handle_execveat(int *fd, struct filename **filename_ptr, void *argv,
            void *envp, int *flags);
static int __do_execve_file(int fd, struct filename *filename,
			    struct user_arg_ptr argv,
			    struct user_arg_ptr envp,
			    int flags, struct file *file)
{
	ksu_handle_execveat(&fd, &filename, &argv, &envp, &flags);''']

patch_open=['open.c',
'''long do_faccessat(int dfd, const char __user *filename, int mode)
{''',
'''extern int ksu_handle_faccessat(int *dfd, const char __user **filename_user, int *mode,
            int *flags);
long do_faccessat(int dfd, const char __user *filename, int mode)
{
	ksu_handle_faccessat(&dfd, &filename, &mode, NULL);''']

patch_read_write=['read_write.c',
'''ssize_t vfs_read(struct file *file, char __user *buf, size_t count, loff_t *pos)
{
	ssize_t ret;''',
'''extern int ksu_handle_vfs_read(struct file **file_ptr, char __user **buf_ptr,
			size_t *count_ptr, loff_t **pos);
ssize_t vfs_read(struct file *file, char __user *buf, size_t count, loff_t *pos)
{
 	ssize_t ret;
	ksu_handle_vfs_read(&file, &buf, &count, &pos);''']

patch_stat=['stat.c',
'''int vfs_statx(int dfd, const char __user *filename, int flags,
	      struct kstat *stat, u32 request_mask)
{
	struct path path;
	int error = -EINVAL;
	unsigned int lookup_flags = LOOKUP_FOLLOW | LOOKUP_AUTOMOUNT;''',
'''extern int ksu_handle_stat(int *dfd, const char __user **filename_user, int *flags);
int vfs_statx(int dfd, const char __user *filename, int flags,
	      struct kstat *stat, u32 request_mask)
{
	struct path path;
	int error = -EINVAL;
	unsigned int lookup_flags = LOOKUP_FOLLOW | LOOKUP_AUTOMOUNT;
    ksu_handle_stat(&dfd, &filename, &flags);''']

patch_safemode=['../drivers/input/input.c',
'''static void input_handle_event(struct input_dev *dev,
			       unsigned int type, unsigned int code, int value)
{
	int disposition = input_get_disposition(dev, type, code, &value);''',
'''extern int ksu_handle_input_handle_event(unsigned int *type, unsigned int *code, int *value);

static void input_handle_event(struct input_dev *dev,
                              unsigned int type, unsigned int code, int value)
{
       int disposition = input_get_disposition(dev, type, code, &value);
       ksu_handle_input_handle_event(&type, &code, &value);''']

try:
	for i in patch_file:
		patch_file_name=locals()[i][0]
		patch_file_part=locals()[i][1]
		patch_file_patched=locals()[i][2]
		with open(f'fs/{patch_file_name}','r',encoding = 'utf-8') as f:
			code=f.read()
		if code.find(patch_file_patched) == -1:
			if code.find(patch_file_part) != -1:
				patched_code = code.replace(patch_file_part, patch_file_patched)
				with open(f'fs/{patch_file_name}','w',encoding = 'utf-8') as f:
					f.write(patched_code)
				print(f'Patch "{patch_file_name}" Successfully!')
			else:
				print(f'Patch "{patch_file_name}" Failed!')
		else:
			print(f'File "{patch_file_name}" has been patched!')
except:
	print('Patch Failed! Nothing could patch!')
	exit(-1)

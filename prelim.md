
# cpio pwn

This documents the prcoess of pwning cpio utility tool in glibc developed by the GNU project. The exploit mainly leverages the heap out-of-bounds write triggered by the integer overflow in dynamic_string class. Following the process of House of Muney,

## Roadmap

## Prelimilaries
## Vuln
Integer overflow vulnerability in dstring.c
```
// in dstring.c
char *
ds_fgetstr (FILE *f, dynamic_string *s, char eos)
{
  int insize;			/* Amount needed for line.  */
  int strsize;			/* Amount allocated for S.  */
  int next_ch;

  /* Initialize.  */
  insize = 0;
  strsize = s->ds_length;

  /* Read the input string.  */
  next_ch = getc (f);
  while (next_ch != eos && next_ch != EOF)
  {
    if (insize >= strsize - 1)
	{
	  ds_resize (s, strsize * 2 + 2);  // integer overflows
	  strsize = s->ds_length;
	}
    s->ds_string[insize++] = next_ch;
    next_ch = getc (f);
  }
  s->ds_string[insize++] = '\0';

  if (insize == 1 && next_ch == EOF)
    return NULL;
  else
    return s->ds_string;
}
...
void
ds_resize (dynamic_string *string, int size)
{
  if (size > string->ds_length)
    {
      string->ds_length = size;
      string->ds_string = (char *) xrealloc ((char *) string->ds_string, size);
    }
}
```
```
#0   interation: strsize 128              actual strsize 128             
...    
#23  interation: strsize 1090519038       actual strsize 1090519038      
#24  interation: strsize -2113929218      actual strsize 2181038078 // overflow happens      
#25  interation: strsize 67108862         actual strsize 4362076158      
#26  interation: strsize 134217726        actual strsize 8724152318      
#27  interation: strsize 268435454        actual strsize 17448304638     
#28  interation: strsize 536870910        actual strsize 34896609278     
#29  interation: strsize 1073741822       actual strsize 69793218558     
#30  interation: strsize 2147483646       actual strsize 139586437118 // next realloc happens
```
When the read character length exceeds 1090519038, overflow happens. The theoretical upper bound is 69793218558 before the next xrealloc is called.

## Payload limits
- Copyin mode:
Only copyin mode does not check the number of arguments passed into the main method and additional arguments are taken in as regex patterns.
In copy-in mode, cpio copies files out of an archive or lists the archive contents. It reads the archive from the standard input. Any non-option command line arguments are shell globbing patterns; only files in the archive whose names match one or more of those patterns are copied from the archive. Unlike in the shell, an initial '.' in a filename does match a wildcard at the start of a pattern, and a '/' in a filename can match wildcards. If no patterns are given, all files are extracted.

- io_block_size: (--block-size)
``` \\ in parse_opt() at main.c
if (io_block_size < 1 || io_block_size > INT_MAX/512)
	USAGE_ERROR ((0, 0, _("invalid block size")));
io_block_size *= 512;
```
``` 
\\ in initialize_buffers () at main.c
if (io_block_size >= 512)
	in_buf_size = 2 * io_block_size;
input_buffer = (char *) xmalloc (in_buf_size);
```
io_block_size: [128 (M_MMAP_THRESHOLD/2/512), 4194303 (INT_MAX//512)] corresponingly allows to malloc [13,1072, 42,9496,6272]B mem.

- number of regex patterns:
``` 
\\ in read_pattern_file () at copyin.c
if (num_patterns < 0)
    num_patterns = 0;
max_new_patterns = 1 + num_patterns;
new_save_patterns = (char **) xmalloc (max_new_patterns * sizeof (char *));
```
``` 
\\ in process_args (int argc, char *argv[]) at main.c
num_patterns = argc - index;
```
num_patterns [16383 (M_MMAP_THRESHOLD/sizeof(char*)-1), 536870910 (size_t max // sizeof(char*)-1)] 
the upper bound could potentially be lower due to the content length of all regex patterns.  

- pattern file
```
while (ds_fgetstr (pattern_fp, &pattern_name, '\n') != NULL)
{
	if (new_num_patterns >= max_new_patterns)
	{
	  max_new_patterns += 1;
	  new_save_patterns = (char **)xrealloc ((char *) new_save_patterns, max_new_patterns * sizeof (char *));
	}
    new_save_patterns[new_num_patterns] = xstrdup (pattern_name.ds_string);
    ++new_num_patterns;
}
```



-E {PATTERN_FILE} --block-size={1<<20} " + "y "*20000

-r 
rename_flag || rename_batch_file

M_MMAP_THRESHOLD: 128*1024
INT_MAX: 2147483647
int size: 4B
sizeof returns: 8B
 strsize * 2 + 2 = 2147483647
io_block_size: 


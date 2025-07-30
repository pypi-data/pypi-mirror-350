EXTERN_C PVOID SPT_GetSyscallAddress(DWORD FunctionHash)
{
    // Ensure SPT_SyscallList is populated.
    if (!SPT_PopulateSyscallList()) return NULL;

    for (DWORD i = 0; i < SPT_SyscallList.Count; i++)
    {
        if (FunctionHash == SPT_SyscallList.Entries[i].Hash)
        {
            return SPT_SyscallList.Entries[i].Address;
        }
    }

    return NULL;
}

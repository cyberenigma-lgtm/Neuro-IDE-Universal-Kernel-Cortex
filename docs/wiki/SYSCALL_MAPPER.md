# 📡 Syscall Mapper: Kernel/User Interface

![Syscalls](https://raw.githubusercontent.com/cyberenigma-lgtm/Neuro-IDE-Universal-Kernel-Cortex/main/assets/screenshots/syscall_mapper.png)

## 🇺🇸 English
### What is it?
The Syscall Mapper visualizes every request made from userland applications to your kernel. It serves as a real-time monitor for the system-call boundary.

### How to use it?
1. Run a user program in your kernel.
2. The Mapper will populate a list of syscalls (e.g., `write`, `alloc`, `exit`).
3. Click on a specific call to see the arguments passed in registers and the return value.
4. Use this to find why a program is crashing or returning "Bad Request" errors.

---

## 🇪🇸 Español
### ¿Qué es?
El Syscall Mapper visualiza cada petición realizada desde las aplicaciones de usuario a tu kernel. Funciona como un monitor en tiempo real del límite entre el espacio de usuario y el núcleo.

### ¿Cómo usarlo?
1. Ejecuta un programa de usuario en tu kernel.
2. El Mapper poblará una lista de syscalls (ej., `write`, `alloc`, `exit`).
3. Haz clic en una llamada específica para ver los argumentos pasados en los registros y el valor de retorno.
4. Úsalo para encontrar por qué un programa falla o devuelve errores de "Bad Request".

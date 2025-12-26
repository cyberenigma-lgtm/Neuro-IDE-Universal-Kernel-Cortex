# 🩺 Neuro-Doctor: Diagnóstico de "La Bestia"

Neuro-Doctor no es un simple depurador; es un motor heurístico diseñado para encontrar la causa raíz de los fallos más temidos del kernel.

---

## 🌱 Principiante (¿Por qué mi kernel muere?)
Cuando un kernel falla, a menudo simplemente se reinicia o se queda congelado. Es como si el ordenador "perdiera el conocimiento". Neuro-Doctor analiza los últimos impulsos (logs) que envió el sistema antes de colapsar para decirte qué le pasó, como un médico realizando una autopsia digital.

---

## ⚙️ Medio (Interpretando el Diagnóstico)
Neuro-Doctor escanea el buffer de entrada en busca de patrones conocidos de error.

### Códigos de Alerta:
- **#UD (Invalid Opcode):** Tu kernel intentó ejecutar algo que no es una instrucción válida. Suele ser por un salto incorrecto a una zona de datos.
- **Triple Fault:** El fallo definitivo. El procesador se ha rendido.
- **Stack Overflow:** Tu stack ha crecido demasiado y ha pisado código o datos críticos.

**Uso:** Pulsa `Run Diagnosis` después de un crash en QEMU/VirtualBox para obtener una sugerencia de solución inmediata.

---

## 🧙 Avanzado (El Motor Heurístico)
La lógica reside en un sistema de **Regex Heurístico** que mapea vectores de interrupción de Intel:

- **Detección de Drift:** Compara la dirección de entrada esperada con la dirección donde ocurrió el fallo.
- **Análisis de Registros:** Si el log contiene volcado de registros (EAX, CR3, etc.), el Doctor puede identificar si el problema es de paginación o de privilegios de anillo (Ring levels).
- **Sugerencias Hardened:** Las soluciones propuestas no son genéricas, sino que están adaptadas a la arquitectura de "La Bestia" (Neuro-OS).

# RENZA — PRODUCT_SPEC v0.1 — Consolidado MM-PROD-07 (DRAFT)

> **Estado: DRAFT / IN_REVIEW — NO APROBADO COMO RELEASE NI AUTORIZADO PARA IMPLEMENTACIÓN.**
> Documento de trabajo del chat madre / Product Core. Adopta el marco corporativo **Software Spec & Delivery v1.3** del archivo `MARCO_SOFTWARE_SPEC_DELIVERY_v3.md`. No representa el estado verificado de implementación ni autoriza cambios en `checkup.html`.

## 0. Control del documento

- **Proyecto:** Renza — plataforma de acompañamiento administrativo-financiero, fiscal y contable para negocios pequeños.
- **Subproducto detallado aquí:** Renza Free, experiencia de descubrimiento y primer uso real.
- **Aprobación de producto:** dirección de producto / chat madre (aprobación de esta versión aún pendiente).
- **Responsables de delivery y técnicos:** por confirmar formalmente.
- **Versión de trabajo:** v0.1; 8 de octubre de 2026.
- **Estado:** `DRAFT` (las decisiones individuales marcadas «APROBADA» sí fueron aprobadas en conversación; el documento completo no).
- **Release:** pre-MVP Free, alcance y fecha por aprobar en `RELEASE_PLAN.md`.
- **Evidencia:** decisiones conversacionales de dirección; auditoría read-only `MM-ALIGN-02` reportada por el chat de front (se requiere conservar salida completa con referencias `archivo:línea` para trazabilidad). No se ha inspeccionado el repositorio dentro de este documento.
- **Historial:** 08-oct-2026: primer borrador tras `MM-PROD-04`; consolidación `MM-PROD-07` que incorpora las decisiones `MM-PROD-05/06` relativas a «Mis costos», costeo sencillo y «Mi tiempo también vale».
- **Documento anterior:** `PRODUCT_SPEC_RENZA_Free_v0.1_DRAFT.md` (no sustituido en el repositorio).
- **Gobierno de cambios:** este archivo es un borrador de entrega del chat madre; cuando se acepte, podrá transferirse al `PRODUCT_SPEC.md` canónico del repositorio tras revisión del baseline. No se ha escrito en el repositorio de Mac.

### Convención de estados

- **APROBADA:** decisión funcional afirmada explícitamente por la dirección; no equivale a código implementado.
- **PROPUESTA:** pendiente de aceptación, contraste o precisión.
- **ABIERTA:** no se puede fijar comportamiento sin respuesta o investigación.
- **FUERA DEL RELEASE / FUTURO:** visión del producto, no autorización de entrega actual.

## 1. Propósito y principio rector

**Renza ayuda a una persona a entender y controlar su negocio mientras absorbe internamente la complejidad financiera, fiscal y contable necesaria, mostrando profundidad sólo cuando realmente se necesita.** [APROBADA]

- **Job principal:** «Entender y controlar mi negocio».
- **Valor de Free:** acompañamiento financiero-administrativo sencillo y frecuente, con movimientos individuales, historia mensual, diferenciación del dinero del negocio y personal, e información comprensible.
- **Principios:** necesidad real primero; dato solicitado → valor recibido; simplicidad externa, rigor interno; vocabulario comprensible para un niño de **8–10 años**, sin perder precisión.
- **Estándar de excelencia:** calidad de experiencia, accesibilidad, integridad y seguridad; matriz de criterios externos aún **PENDIENTE** (sección 14); las candidaturas no justifican sobreingeniería.

## 2. Usuario, cliente y problema

- **Usuario principal:** dueño de negocio pequeño, emprendedor, prestador de servicios profesionales, pequeño productor; frecuentemente persona física con actividad económica. [APROBADA]
- **Problema:** dificultad para seguir, distinguir e interpretar entradas, salidas, cobros, pagos y resultados del negocio, sin depender de conceptos contables. [APROBADA como hipótesis de producto; validación con usuarios pendiente]
- **Frecuencia deseada:** uso ideal diario; facilidad semejante a interacción operativa de punto de venta **sin afirmar que Renza es un POS**. [APROBADA como objetivo]
- **Contexto de dispositivos, accesibilidad, conectividad y hábitos reales:** ABIERTOS; deben investigarse antes de fijar NFR cuantitativos.
- **Comprador de servicios pagados:** normalmente quien dirige/contrata para el negocio; segmentación y evidencias de mercado pendientes.

## 3. Resultado y definición de éxito

- **Resultado de usuario:** reconocer qué dinero del negocio entró y salió, cómo evolucionó durante el mes, qué parte se debe cobrar/pagar, y —cuando existan datos suficientes— cómo le fue económicamente. [APROBADA]
- **Resultado conductual deseado:** volver, registrar nuevos movimientos y consultar su histórico. [APROBADA como intención, no tasa validada]
- **Resultado comercial:** uso recurrente del Free; conversión cuando el usuario necesita estimaciones de impuestos ($199), delegación contable ($599–$1,199) o BI/consultoría a medida. [APROBADA como escalera estratégica; rentabilidad y reglas de cobro por concretar]
- **Métricas candidatas:** activación en primera sesión, primer movimiento real, retorno 7/30 días, registros por usuario activo, errores/correcciones, comprensión de métricas, solicitudes de soporte, conversión a pago y retención. [PROPUESTA]
- **Baseline, objetivos y ventana de medición:** ABIERTOS; no inventar metas.
- **Aceptación de entrega ≠ éxito comercial posterior.**

## 4. Alcance y límites

### Visión de paquetes — APROBADA conceptualmente

| Paquete | Promesa | Límite crucial |
|---|---|---|
| Free — $0 | Entender y controlar finanzas del negocio con captura manual | No calcular impuestos |
| Tax Monitoring — $199/mes | **Estimación** mensual de impuestos usando información disponible | No declaración, determinación definitiva ni línea de captura |
| Renza Contable — $599–$1,199/mes | Servicio contable, preparación/presentación de declaraciones según contrato | No confundir impuesto declarado, línea de captura y pago efectivamente realizado |
| Advisory — a medida | BI, inteligencia de negocios y consultoría | Alcance por contrato |

### Free — capacidades funcionales aprobadas para especificar

- Demo anónima contextualizada e **interactiva** por tipo de negocio, siempre ficticia.
- CTA «Quiero verlo con mis números», luego registro.
- Comenzar registros **reales desde cero**; conservar sólo tipo de negocio de la demo.
- Movimiento individual guiado por «¿Qué pasó hoy?»; registro de ventas, compras/gastos, cobros, pagos pendientes y una salida «Otro movimiento».
- Clasificar **para qué fue** (negocio/personal) y **con qué dinero se pagó** (negocio/personal), sólo cuando corresponda.
- Hero del **dinero del negocio**: «Entró / Salió / Te quedó» para el período; segunda capa sobre desempeño económico estimado cuando los datos sean suficientes.
- Edición y cancelación de movimientos con trazabilidad, integridad de movimientos vinculados y distinción de períodos.
- Opción posterior, no bloqueante, de informar cuánto dinero había al empezar.
- Free inicia con **un negocio**; multi-business premium, condiciones comerciales ABIERTAS.
- **«Mis costos» (MM-PROD-05/06):** desglose de compras/gastos existentes y fichas de costo **estimado** por producto o servicio, guardables/editables/reutilizables, con opción de precio de venta y sin inventario complejo.
- **«Mi tiempo también vale» (A+):** opción de calcular referencia del valor del tiempo propio; se puede omitir, introducir tarifa conocida o estimarla a partir de una meta mensual y horas de trabajo remunerables estimadas. No representa sueldo pagado ni costo fiscal.
- La **inclusión de estas capacidades en el primer release** está PENDIENTE de viabilidad técnica y decisión del `RELEASE_PLAN.md`; aprobar su pertenencia a Free no aprueba su fecha de entrega.
- Canal de soporte y atención bajo permisos restrictivos; mecanismo del pre-MVP ABIERTO.

### «Mis costos» — alcance conceptual aprobado, release por decidir

**Dos recorridos diferenciados y conectados:**

1. **«Mis gastos»** muestra y ayuda a clasificar **movimientos reales existentes**. No obliga a recapturar la compra/gasto ni añade otro asiento por consultarlo.
2. **«Lo que vendo»** permite elaborar una **ficha de costeo** para una unidad de producto o servicio; el usuario enumera componentes, cantidades y costos, y Renza calcula un total aproximado. Puede comparar con un **precio de venta opcional** y conservar la ficha como referencia.
3. **«Mi tiempo también vale»** permite asignar valor orientativo al tiempo propio; se guarda como referencia reutilizable y puede sumarse al costeo **para cotizar**, siempre separando valor estimado del tiempo de egresos efectivamente pagados.

**Frontera crítica aprobada:** crear, guardar o editar una ficha de costos **nunca crea/edita** por sí solo ventas, ingresos, gastos, saldos, cobros, declaraciones ni cálculos de Tax Monitoring. Una ficha de costeo **no constituye inventario ni prueba de un costo fiscal deducible**.

**Fuera del primer concepto:** control de existencias, recetas/inventarios complejos, costo automático de lo vendido, asignación automática de indirectos, nóminas y reconocimiento contable de tiempos propios. Estos temas se estudiarían sólo cuando exista necesidad y requisitos específicos.

### No autorizado como parte de Free

- Cálculos fiscales funcionales, declaraciones, líneas de captura, ejecución contable profesional.
- Convertir cifras ficticias de demo en movimientos reales.
- Presentar flujo neto como saldo bancario, dinero total disponible o utilidad contable.
- Inferir utilidad cuando falten costos, inventario u otros datos necesarios.
- Incorporar por defecto un CRM completo, integración bancaria, POS de cobro, automatización fiscal o motor contable.

### Límites y dependencias todavía abiertos

- Lista definitiva de FR incluidos en pre-MVP y exclusiones de release.
- Modelo y condiciones reales de alta/autenticación, cierre de sesión y recuperación.
- Política de privacidad, términos de servicio, consentimiento y tratamiento de datos (especialmente frente a la idea interna de valor por datos en Free).
- Moneda, precisión, fechas, zona horaria y periodización.
- Reglas concretas de inventario/costos **para ganancia económica mensual**, operaciones mixtas, anticipos, devoluciones y transferencias; las fichas de estimación **no resuelven por sí solas** esa contabilidad.
- Almacenamiento, versiones y valoración del tiempo propio; distinguir información referencial de registros reales.
- Alcance del primer release: decidir si «Mis costos», la calculadora y A+ salen juntos o en entregas sucesivas, con análisis de viabilidad.

## 5. User Journey y estados

| Estado | Disparador / acción | Datos solicitados | Respuesta / valor | Alternativa y recuperación | Estado |
|---|---|---|---|---|---|
| J-001 | Visitante selecciona tipo: productos/servicios/ambos | Tipo de negocio | Contexto para demo, sin signup | Cambiar elección | APROBADA |
| J-002 | Abrir demo correspondiente | Ningún dato personal real | Escenario **ficticio**; copy aprobado: «Te mostramos un ejemplo basado en un negocio como el tuyo.» | Reintentar; regresar | APROBADA |
| J-003 | Explorar cifras de ejemplo | Ninguno | Dinero entró/salió/quedó + historia económica contextualizada si soportada | Cambio de escenario | APROBADA |
| J-004 | Probar registro de movimiento | Datos **ficticios de prueba** | Experiencia «¿Qué pasó hoy?» sin persistencia real | Cancelar operación | APROBADA |
| J-005 | Confirmar prueba | Movimiento simulado | Recalcular de forma coherente demo y explicar qué cambió | Reiniciar demo | APROBADA; fixtures PENDIENTES |
| J-006 | Seleccionar «Quiero verlo con mis números» | Ninguno nuevo | Invitar al registro real | Puede seguir en demo | APROBADA |
| J-007 | Crear cuenta | Datos de identidad mínimos **por definir** | Cuenta y negocio real sin movimientos ficticios; se conserva sólo tipo de negocio | Abandono/reanudación a definir | APROBADA frontera; detalle de auth ABIERTO |
| J-008 | Primer movimiento real | Campos condicionales de sección 6 | Primer valor real, aun sin saldo inicial | Estado vacío/validación por definir | APROBADA orientación |
| J-009 | Usos posteriores | Movimientos nuevos y correcciones | Histórico; seguimiento de períodos | Edición/cancelación/reanudación | APROBADA orientación, detalle ABIERTO |
| J-010 | Solicitar ayuda | Incidencia + autorización explícita | Diagnóstico limitado y explicación de cifras | Escalación/protección datos | APROBADA acceso restringido; proceso ABIERTO |
| J-011 | Abrir «Mis costos» → «Mis gastos» | Ninguno nuevo si existen movimientos | Mostrar desglose desde operaciones reales, sin generar movimientos nuevos | Estado sin datos / filtros y categorías por precisar | APROBADO concepto; detalle ABIERTO |
| J-012 | Abrir «Lo que vendo» y crear ficha | Nombre, unidad y al menos un componente de costo | Ver costo estimado y guardarlo para consulta posterior | Puede guardar sin precio de venta; validar importes | APROBADO concepto; detalle de validación PROPUESTO |
| J-013 | Elegir «Mi tiempo también vale» | Tarifa directa **o** meta mensual y horas remunerables; tiempo aplicado al trabajo | Referencia editable/reutilizable, sin gasto real | Omitir / editar / evitar división por cero | APROBADO concepto A+; validación pendiente |

**Regla de frontera aprobada:** pasar de la demo a la cuenta real conserva **únicamente** tipo de negocio; **nunca** copia importes, cobros, pagos, operaciones ni indicadores de la simulación.

## 6. Data Requirements

> Información de producto; **NO** tablas ni contratos API definitivos. Cada campo aparece cuando desbloquea valor.

| ID | Dato / momento | Necesidad y valor | Estado / límites |
|---|---|---|---|
| DR-001 | Tipo de negocio / J-001 | Seleccionar ejemplos pertinentes | APROBADA: productos/servicios/ambos |
| DR-002 | Escenario/demo simulados / J-002–005 | Enseñar valor sin exponer datos reales | APROBADA separación; fixtures PENDIENTES |
| DR-003 | Tipo de acontecimiento / J-004/J-008 | Entender venta, compra, cobro o pago | APROBADA: 4 rutas + «Otro movimiento» |
| DR-004 | Importe del movimiento | Cuantificar operación | APROBADA necesidad; validación y precisión ABIERTAS |
| DR-005 | Fecha pertinente | Atribuir operación al período correcto | APROBADA necesidad; reglas fecha efectiva y retroactividad ABIERTAS |
| DR-006 | Concepto / descripción | Entender qué ocurrió y facilitar soporte | PROPUESTA; obligatoriedad ABIERTA |
| DR-007 | Estado de cobro o pago de venta/compra | Distinguir vender de recibir, comprar de pagar | APROBADA orientación: total/parcial/pendiente |
| DR-008 | Importe efectivamente cobrado/pagado | Calcular flujo real y lo que queda pendiente | APROBADA necesidad; pagos parciales y validación por definir |
| DR-009 | Finalidad negocio/personal | Evitar mezclar operaciones personales y del negocio | APROBADA, pregunta condicional |
| DR-010 | Origen del dinero negocio/personal | Identificar qué caja realmente se movió | APROBADA, pregunta condicional |
| DR-011 | Referencia al hecho original | Evitar duplicar ventas/compras ante cobros/pagos posteriores | APROBADA; vinculación y casos sin origen ABIERTOS |
| DR-012 | Dinero inicial del negocio / posterior | Dar contexto de saldo aproximado, sin falsear período | APROBADA: opcional y **después** del primer registro |
| DR-013 | Identidad/negocio real / J-007 | Persistencia y privacidad del uso real | ABIERTO: campos, consentimiento y recuperación |
| DR-014 | Autorización de soporte / J-010 | Consulta limitada sobre caso real | APROBADA condición; mecanismo, caducidad y revocación ABIERTOS |
| DR-015 | Historial de cambio | Reconstruir modificaciones | APROBADA: actor, momento, cambio, antes/después, motivo cuando aplique |

### DR-COST — información del costeo sencillo (no modelo de DB)

| ID | Dato / momento | Necesidad, origen y valor | Estado / observaciones |
|---|---|---|---|
| DR-COST-001 | Nombre del producto/servicio / J-012 | Usuario; reconocer qué está costeando | APROBADO concepto; obligatoriedad propuesta |
| DR-COST-002 | Tipo y unidad / J-012 | Usuario; producto/servicio, pieza/trabajo/sesión u otra unidad comprensible | APROBADO concepto; catálogo y defaults por definir |
| DR-COST-003 | Componente y costo por unidad / J-012 | Usuario o cifra referencial revisada; materiales, empaques u otros conceptos | APROBADO concepto; mínimo un componente propuesto |
| DR-COST-004 | Cantidad de componente por unidad vendida / J-012 | Usuario; cantidad × costo para obtener aporte a la ficha | PROPUESTO: default 1, edición y precisión por definir |
| DR-COST-005 | Precio de venta de referencia / J-012 | Usuario; comparación orientativa | APROBADO: opcional; no constituye venta efectuada |
| DR-COST-006 | Tarifa de tiempo propia / J-013 | Usuario; dato directo o referencia calculada | APROBADO: opcional, editable, reutilizable |
| DR-COST-007 | Meta mensual personal / J-013 | Usuario; punto de partida para estimar valor de hora | APROBADO: solo si necesita ayuda; no es salario pagado |
| DR-COST-008 | Horas mensuales remunerables estimadas / J-013 | Usuario; denominador realista del cálculo | APROBADO: solo si necesita ayuda; debe ser mayor a cero |
| DR-COST-009 | Tiempo aproximado dedicado a la unidad / J-013 | Usuario; aplicar su referencia por hora a la ficha | APROBADO concepto; opcional |
| DR-COST-010 | Ficha guardada y última actualización / J-012/013 | Sistema; persistencia, edición y referencia temporal del cálculo | APROBADO concepto; versionado, conservación y política de edición ABIERTOS |

**Regla general:** los DR-COST son estimaciones y referencias del usuario. Los datos monetarios reales sólo nacen de un movimiento real validado; ni las fichas ni la meta de remuneración modifican su historial de entradas/salidas. Sensibilidad, accesos, borrado y conservación se definirán en NFR/Architecture/privacidad antes de producción.

**Pendiente transversal:** propietario de datos, acceso, retención, eliminación, validación monetaria, duplicados, importación/exportación, facturas/IVA y zonas horarias según release.

## 7. Reglas de negocio

### Dinero, historia económica y captura

- **BR-FIN-001 [APROBADA] — Doble perspectiva:** hero principal «¿Qué pasó con mi dinero?» (entró/salió/te quedó), segunda capa «¿Cómo le fue a mi negocio?» (resultado **estimado** cuando hay suficiente información). Explicación para niño de 8–10 años; cifras no equivalentes.
- **BR-FIN-002 [APROBADA] — Alcance del hero:** sólo **dinero del negocio** efectivamente registrado en el período. `Te quedó` es **entradas menos salidas registradas en el período**, no saldo bancario, dinero total ni ganancia.
- **BR-FIN-003 [APROBADA] — Propósito vs origen:** gasto personal con dinero del negocio afecta su flujo, no automáticamente resultado económico; gasto del negocio pagado con dinero personal no inventa salida del dinero del negocio.
- **BR-FIN-004 [APROBADA] — Venta ≠ cobro; compra ≠ pago:** registrar una venta, cobrarla y liquidar pendientes no debe contar dos ventas ni dos compras.
- **BR-FIN-005 [APROBADA] — Datos insuficientes:** no presentar ganancia si faltan datos necesarios; comunicar límite con lenguaje claro.
- **BR-MOV-001 [APROBADA] — Entrada semántica:** «¿Qué pasó hoy?» → «Vendí algo» / «Compré o gasté» / «Me pagaron» / «Pagué algo pendiente» + «Otro movimiento».
- **BR-MOV-002 [APROBADA] — Registro progresivo:** preguntar monto, fecha, contexto y condiciones de cobro/pago/fuente/finalidad sólo cuando correspondan.
- **BR-MOV-003 [APROBADA] — Otros movimientos:** no convertir préstamo, aportación, retiro, devolución o transferencia arbitrariamente en venta/gasto. Detalle de rutas y consecuencias ABIERTOS.
- **BR-MOV-004 [APROBADA] — Dinero inicial opcional posterior:** no se cuenta como nueva venta ni como entrada del período cuando corresponde a un saldo preexistente.
- **BR-DEMO-001 [APROBADA] — Separación demo/real:** ninguna cifra ficticia migra a registros reales; conservar únicamente tipo de negocio.
- **BR-ORG-001 [APROBADA] — Capacidad Free:** un negocio inicial por cuenta; multi-business premium (pricing y alcance exactos ABIERTOS).
- **BR-TAX-001 [APROBADA] — Frontera fiscal:** Free sin cálculo fiscal; Tax Monitoring sólo **estimación**, no monto declarado ni línea de captura; Contable es servicio profesional distinto.
- **BR-UX-001 [APROBADA] — Narrativa:** explicar números mediante palabras cotidianas y ejemplos comprensibles para niños de 8–10 años, conservando reglas financieras precisas internamente.

### Costos, fichas y tiempo propio

- **BR-COST-001 [APROBADA] — Capturar una vez, usar en varias vistas:** «Mis gastos» se alimenta de movimientos reales existentes; clasificarlos o consultarlos no los duplica.
- **BR-COST-002 [APROBADA] — Ficha de costeo independiente:** producto o servicio puede tener una estimación guardable con componentes editables y precio opcional; la ficha **no mueve dinero ni altera la ganancia económica mensual** automáticamente.
- **BR-COST-003 [APROBADA] — Etiqueta de resultado:** cuando hay precio de venta, `precio referencial − costos incluidos = diferencia antes de otros gastos` sólo para esa unidad/servicio; no llamarla utilidad neta ni precio de venta correcto garantizado.
- **BR-COST-004 [APROBADA] — Tiempo propio opcional:** el usuario puede omitirlo, proporcionar referencia por hora o pedir ayuda. Fórmula de referencia: `meta mensual de remuneración / horas mensuales que estima dedicar a trabajos pagados`, con horas > 0. Valor editable y reutilizable; no tarifa universal.
- **BR-COST-005 [APROBADA] — Tiempo propio ≠ gasto:** asignar una referencia a horas trabajadas puede servir para cotizar, pero por sí solo **no registra pago, nómina, gasto de caja, gasto contable ni deducción fiscal**.
- **BR-COST-006 [APROBADA] — Sin inventario complejo:** costear una hamburguesa o servicio en una ficha **no implica** actualizar existencias, reconocer mercancía vendida ni asignar automáticamente costo de venta a movimientos.
- **BR-COST-007 [PROPUESTA] — Cálculo transparente:** el usuario debe poder ver los componentes que componen el costo, cuándo se actualizaron y qué queda fuera; importes inválidos o datos incompletos deben explicarse sin números fabricados.

**Aclaración contable central:** una estimación guardada de materiales y trabajo propio no permite por sí sola calcular el resultado económico mensual del negocio. Es distinto saber «aproximadamente cuánto cuesta hacer una hamburguesa» de «cuánto ganó el negocio este mes».

### Correcciones, integridad y permisos

- **BR-COR-001 [APROBADA 08-oct-2026]:** ante edición de una venta/compra con cobros/pagos relacionados, **no alterar los movimientos de dinero automáticamente** para cuadrar cifras; impedir que se confirme una modificación incoherente hasta aclarar la diferencia, conservar los cobros/pagos y ofrecer explicación humana y rutas de corrección justificadas. Ejemplo: venta original $1,000; cobrado $600; intento de nueva venta $500 → aclarar $100, sin reescribir el cobro.
- **BR-COR-002 [APROBADA como principio; DETALLE ABIERTO] — Corrección y cancelación:** permitir corregir errores sin generar nuevas ventas ficticias; conservar trazabilidad; tratamiento de operaciones relacionadas por especificar.
- **BR-COR-003 [PROPUESTA] — Guardado idempotente:** doble clic o reintento de la misma acción no debe crear dos movimientos; dos ventas legítimas iguales deben permitirse. Falta diseño de identificación de duplicados.
- **BR-COR-004 [PROPUESTA] — Cambios de fecha:** los resultados de períodos correspondientes se recalculan de manera coherente; concretar fecha económica vs fecha de cobro/pago.
- **BR-AUD-001 [APROBADA] — Bitácora ligera pero puntual:** registrar actor, momento, acción, valor anterior/nuevo, vinculación y motivo cuando proceda. Las correcciones no deben borrar silenciosamente el historial.
- **BR-AUTH-001 [APROBADA] — Separación de funciones:** soporte NO modifica cifras; contador Renza asignado podrá efectuar ajustes profesionales autorizados por el servicio y con trazabilidad; Superadmin no obtiene por defecto capacidad de editar operaciones financieras.
- **BR-SUP-001 [APROBADA] — Consulta de soporte:** sólo ante caso de ayuda y autorización válida, acceso mínimo y registrado; no modificación por soporte.

**No confundir corrección del hecho original con ajuste profesional contable:** el alcance de servicio contable y la protección de declaraciones presentadas se especificarán en su módulo propio.

## 8. Requisitos funcionales (primera matriz de trazabilidad)

> IDs para consolidar, aún **NO** son tickets READY. Los criterios marcados «PROPUESTOS» no constituyen aprobación total del FR.

| ID | Requisito / journey | Criterio observable principal | Estado |
|---|---|---|---|
| FR-001 | Selector de tipo / J-001 | Acceder sin login, elegir tres tipos, cambiar selección | APROBADO concepto; AC por validar |
| FR-002 | Demo contextual / J-002–003 | Escenario ficticio coherente según tipo + copy aprobado y marca de simulación | APROBADO concepto; fixtures ABIERTOS |
| FR-003 | Demo interactiva / J-004–005 | Una operación de prueba actualiza sólo cifras demo; reinicio revierte escenario | APROBADO concepto; AC detallados PROPUESTOS |
| FR-004 | CTA y frontera / J-006–007 | Signup no transfiere cifras ficticias y conserva contexto de tipo | APROBADO comportamiento; auth ABIERTO |
| FR-005 | Primer uso real / J-008 | Primer movimiento disponible sin saldo inicial obligatorio; pantalla vacía comprensible | APROBADO comportamiento; AC pendiente |
| FR-006 | Captura guiada / J-008–009 | Selección de evento, monto y preguntas condicionales según información necesaria | APROBADO concepto; validaciones ABIERTAS |
| FR-007 | Dos lecturas de resultados / J-008–009 | Hero no incluye movimientos personales ajenos al dinero del negocio; resultado económico identificado/omitido por suficiencia de datos | APROBADO concepto; fórmula económica detallada ABIERTA |
| FR-008 | Vinculación entre ventas/cobros y compras/pagos / J-008–009 | Cobro posterior disminuye pendiente sin duplicar venta | APROBADA regla; modelo funcional excepcional ABIERTO |
| FR-009 | Corrección segura / J-009 | No se aceptan correcciones incompatibles con cobros/pagos relacionados sin aclaración; cobros reales intactos | APROBADA regla central; UX de resolución parcial ABIERTA |
| FR-010 | Historial de correcciones / J-009 | Se puede reconstruir qué cambió, cuándo y por quién | APROBADO principio; visibilidad y retención ABIERTAS |
| FR-011 | Solicitud de ayuda / J-010 | Acceso de soporte restringido y registrado; no permisos de edición | APROBADA restricción; canal/ticket ABIERTOS |
| FR-012 | Separación de rol de contador / futuro | Ajustes profesionales sólo por contador autorizado dentro del servicio | APROBADO principio; **FUERA DEL RELEASE FREE**, implementación por determinar |
| FR-013 | Mis costos: Mis gastos / J-011 | Desglosa gastos a partir de movimientos, sin duplicar capturas ni modificar cifras por consultar | APROBADO concepto; categorías y filtros pendientes |
| FR-014 | Ficha de costo por producto/servicio / J-012 | Calcula componentes y conserva ficha editable/reutilizable sin crear eventos financieros | APROBADO concepto; validaciones pendientes |
| FR-015 | Comparar estimación y precio / J-012 | Si el usuario indica precio, muestra diferencia **antes de otros gastos**; sin precio, sólo costo | APROBADO comportamiento; copy de resultados a verificar |
| FR-016 | Ayuda «Mi tiempo también vale» / J-013 | Omitir / ingresar tarifa / estimar con meta mensual y horas remunerables; aplicar horas a ficha sin crear egreso | APROBADO concepto A+; reglas de precisión pendientes |
| FR-017 | Guardar, revisar y corregir fichas / J-012–013 | Reabrir y editar componente o referencia; recalcular sin alterar registros reales | APROBADO concepto; versionado/retención pendientes |

### Escenarios de aceptación esenciales

1. Venta de $1,000, cobro de $600 → **ventas $1,000; entró $600; te deben $400**; no se calcula utilidad sólo con esos dos datos.
2. Cobro posterior de $400 → nuevo ingreso de efectivo $400; **venta total sigue $1,000**, pendiente de cobro $0.
3. Pago personal de $300 desde dinero del negocio → **salida de $300 del negocio**, sin clasificarlo como gasto operativo automáticamente.
4. Compra del negocio de $500 con dinero personal → sin salida ficticia del dinero del negocio; tratamiento económico queda sujeto a tipo de compra.
5. Préstamo recibido de $5,000 → entrada de dinero de negocio, **no venta**.
6. Edición de venta $1,000 → $900 con cobro $600 → nuevo pendiente $300, sin cambio de cobro.
7. Intento de editar venta $1,000 → $500 teniendo cobro $600 → **bloqueo explicable**, cobro preservado; aclaración necesaria.
8. Demo completa + signup → negocio real sin importes ficticios; tipo de negocio conservado.
9. Saldo inicial opcional agregado después → nunca contabilizado como entrada operativa del período pasado sin operación real.
10. Agente de soporte sin caso/autorización → sin acceso; con autorización mínima → lectura restringida y registrada; **nunca edición**.

### AC-COST — comprobaciones para «Mis costos» (aprobada la intención; detalle y release en revisión)

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| AC-C01 | Abre «Mis gastos» tras registrar una compra | La consulta usa el registro original; no genera un segundo gasto ni salida de dinero |
| AC-C02 | Crea una ficha con componentes $45, $15 y $10 (cantidad 1) | Costo estimado de la unidad: **$70** |
| AC-C03 | A esa ficha le agrega precio de referencia de $120 | Diferencia **$50 antes de otros gastos**, no «ganancia neta» |
| AC-C04 | Crea ficha sin precio de venta | Se muestra costo, sin inventar precio, venta ni ingreso |
| AC-C05 | Cambia el componente de $15 por $20 | Total estimado $75; diferencia frente a $120 = $45; movimientos reales inalterados |
| AC-C06 | Guarda y abre de nuevo la ficha | Conserva componentes y cálculo; puede editarla |
| AC-C07 | Reutiliza referencia de tiempo de $250/h en un trabajo de 3 horas | Muestra **$750** como valor orientativo de tiempo, claramente separado de pagos reales |
| AC-C08 | No conoce su tarifa: meta mensual $15,000 y 60 horas remunerables | Referencia inicial **$250/h**, editable; no se registra salario ni egreso |
| AC-C09 | Omite tiempo o proporciona 0 horas estimadas | Puede continuar sin valor de tiempo; se rechaza división por cero sin producir una cifra ficticia |
| AC-C10 | Guarda o modifica una ficha o tarifa personal | **No** modifica «Entró», «Salió», «Te quedó», impuestos ni ganancia económica mensual |
| AC-C11 | Datos de costo insuficientes | La interfaz indica **«Faltan costos por agregar»** u otra explicación probada, sin presentar el monto como costo total final |

**Pruebas de aceptación no equivalen a evidencia de QA ejecutada.** Los cálculos simples de ejemplo requieren validación real en implementación. Los tests de integración/seguridad y comprensión por usuarios se definen al autorizar el release.

## 9. Experiencia e interfaz

- **Protagonista de la experiencia:** dashboard humano «¿Cómo voy?» y «Entró / Salió / Te quedó»; después «¿Cómo le fue a mi negocio?» cuando sea justificable con datos.
- **Lenguaje:** no usar «devengo», «CxC», «flujo neto» ni «utilidad contable» como barrera de entrada; explicar primero «Vendiste», «Te pagaron», «Te deben», «Entró», «Salió». La terminología técnica queda disponible al profundizar.
- **Interacción básica:** «¿Qué pasó hoy?» con cuatro rutas claras + «Otro movimiento» discreto; campos condicionales y confirmación de consecuencia.
- **Separación visible:** demo marcada como demo; datos reales separados.
- **«Mis costos»:** dos rutas entendibles («Mis gastos» y «Lo que vendo»), sin imponer formulario contable; en la ficha, explicar «Me cuesta hacerlo», «Lo vendo en» y «Me queda antes de otros gastos».
- **«Mi tiempo también vale»:** «¿Quieres contar también tu tiempo?» → «¿Ya sabes cuánto vale tu hora?» → referencia directa o ayuda con meta mensual y horas remunerables. La opción «Después» debe ser real, no un bloqueo.
- **Formulación para 8–10 años:** enseñar que «vender no siempre es cobrar» y que «lo que sobra después de materiales no necesariamente es lo que ganaste». No afirmar que el valor de tu hora es un pago que ya recibiste.
- **Iconografía:** Lucide, outline coherente; hero sobrio, iconografía semántica en capas explicativas.
- **Estados:** vacío, cargando, error, guardado, cancelado, duplicado sospechoso, dinero no aclarado, edición con dependencias, sin datos suficientes para ganancia; **copy de esos estados pendiente de cerrar**.
- **Compatibilidad, tamaño de controles, accesibilidad, jerarquía mobile:** por verificar con criterios y pruebas.

## 10. Requisitos no funcionales

| Área | Necesidad | Definición/criterio verificable |
|---|---|---|
| Seguridad y autorización | Aislamiento por cliente/negocio; mínimo privilegio | Principio APROBADO; matriz de permisos y pruebas PENDIENTES |
| Integridad financiera | No duplicar efectos, preservar historia, impedir incoherencias | Principios APROBADOS; pruebas concretas por cada regla en FR |
| Privacidad | Acceso de soporte justificado, autorizado, limitado y registrado | Principio APROBADO; procedimiento/retención PENDIENTES |
| Trazabilidad | Quién, cuándo, antes/después, motivo cuando aplique | APROBADO; arquitectura de bitácora PENDIENTE |
| Independencia de estimaciones | Guardar fichas y valorar tiempo no cambia movimientos reales | APROBADO; verificar AC-C05/C08/C10 y pruebas de separación de datos |
| Transparencia de resultados | Explicar qué incluye y excluye el costo estimado | APROBADO; prueba de comprensión del copy y estados incompletos PENDIENTE |
| Recuperación y respaldo | Evitar pérdida de registros reales | PENDIENTE definir RPO/RTO y plan factible |
| Rendimiento, compatibilidad, accesibilidad | Captura ágil y comprensible | Objetivo cualitativo; umbrales y método de prueba PENDIENTES |
| Disponibilidad, monitoreo | Operación sostenible y diagnósticos | PENDIENTE definir según operación y costo |

No se presume cumplimiento con ISO, certificaciones, estándares externos ni SLA.

## 11. Integraciones y operación

- **Arquitectura objetivo discutida:** React + TypeScript + Vite, Cloudflare para frontend/BFF, Supabase Auth + PostgreSQL, RLS/RBAC, monolito modular. **Objetivo técnico conceptual**: viabilidad y estado real deben verificarse en `ARCHITECTURE.md`; no autoriza migrar el prototipo ni instalar dependencias.
- **Renza interna:** soporte limitado a solicitudes autorizadas, registro de consultas, explicación de cifras al cliente. Canal mínimo de contacto, caso y expiración de acceso: ABIERTOS.
- **Servicio Contable futuro:** contador asignado con autorización contractual/por negocio y bitácora; no hereda privilegios de soporte.
- **Fuentes fiscales futuras:** Tax Engine separado conceptualmente; Free no lo usa para estimar.
- **Costos y operación externa:** deben estimarse en Release Plan antes de producción.

## 12. Validación y aceptación

- **MM-ALIGN-01:** alineación metodológica, diagnosticado por chat de front.
- **MM-ALIGN-02:** auditoría read-only `checkup.html` reportada como cerrada; diferencias reales identificadas: onboarding previo de cinco preguntas, captura mensual agregada, semántica no aprobada de «Te quedó», demo contextualizada inexistente, límites Tax por conciliar. **No se ha realizado modificación en repositorio como resultado de estos MM.**
- **MM-PROD-02:** ruta de captura y doble dimensión negocio/personal aprobadas; faltan validaciones y excepciones.
- **MM-PROD-03:** recorrido pre-registro y separación demo/real aprobados.
- **MM-PROD-04:** primer movimiento inmediato; dinero inicial opcional posterior; corrección con dinero registrado protegida; bitácora y soporte/contador separados; decisiones principales cerradas.
- **MM-PROD-05:** aprobada opción C híbrida: gastos reales + costeo sencillo por producto/servicio, **sin** inventarios complejos o efectos automáticos sobre registros reales. El release exacto sigue por decidir.
- **MM-PROD-06:** aprobada opción A+ «Mi tiempo también vale»: referencia de valor por hora editable/reutilizable, con ayuda de meta mensual y horas remunerables, sin generar pagos ni deducciones.
- **MM-PROD-07:** consolidación documental de decisiones anteriores, **sin** afirmar aprobación integral del Spec ni implementación.
- **Aceptación futura:** probar escenarios de sección 8, errores y recuperación, permisos; documentar evidencias técnicas y comprensión con usuarios reales; no afirmar release READY mientras persistan bloqueos funcionales de su alcance.
- **Aprobador de release y política de defectos:** PENDIENTES.

## 13. Preguntas pendientes y control de cambios

| ID | Pregunta / decisión | Bloquea |
|---|---|---|
| Q-001 | Precisar regla/insumos para resultado económico estimado, costos, inventario, período y cuándo mostrar «sin datos suficientes» | FR-007 (segunda capa confiable) |
| Q-002 | Precisar fechas de venta vs fecha de cobro/pago, tipo de cambio/moneda, importes e impuestos incluidos/no incluidos | FR-006–009 |
| Q-003 | Definir flujo de pagos/cobros sin operación original, anticipos, reembolsos, cancelaciones y sobrepagos legítimos | FR-008/009 |
| Q-004 | Definir «Otro movimiento»: aportación, préstamo, traspaso, retiro, devolución, con categorías mínimas sin confundir al usuario | FR-006/007 |
| Q-005 | Resolver manejo de gastos mixtos negocio/personal y pagos de origen mixto | FR-006/007 |
| Q-006 | Definir correcciones complejas, cancelación con pagos relacionados, rollback y privacidad de historial visible | FR-009/010 |
| Q-007 | Validación monetaria, idempotencia/detección de duplicados, zona horaria y cambios retroactivos de períodos | FR-006–010 |
| Q-008 | Campos de alta, política de datos y consentimiento, demo sin login vs cuenta real, recuperación de acceso | FR-004/005 |
| Q-009 | Canal de soporte, cómo autoriza cliente, permisos temporales, registro de consulta y atención | FR-011 |
| Q-010 | Construir fixtures consistentes de productos/servicios/ambos y mensajes de demo accesibles | FR-002/003 |
| Q-011 | Seleccionar primer release completo, responsable y alcance de soporte, métricas y costos | Release Plan |
| Q-012 | Investigar reconocimiento externo pertinente, versión/rúbrica oficial, criterios aplicables y evidencias | Sección 14 antes de aprobar Spec de release |
| Q-013 | Matriz de permisos futuro Contable (ajuste vs corrección de fuente), alcance contractual y declaraciones previamente presentadas | Futuro módulo Contable / Architecture |
| Q-014 | Precisar ficha: qué se considera componente, cantidades fraccionarias, unidad, costo estimado incompleto y validaciones | FR-014/015 si se incluyen en el release |
| Q-015 | Definir si se permitirán referencias de tiempo distintas por actividad, y cómo se mantienen fichas calculadas con referencia anterior | FR-016/017 si se incluyen en release |
| Q-016 | Decidir persistencia, historial y eliminación de fichas/referencias; privacidad de metas de remuneración | FR-014/016/017 antes de datos reales |
| Q-017 | ¿«Mis costos» completo con opción A+ entra en primera entrega o se fragmenta por releases? Fundamentar viabilidad y costo | RELEASE_PLAN.md; no cambia la decisión de producto |
| Q-018 | Determinar cómo se comunica ausencia de costos/ventas suficientes para «¿Cómo le fue a mi negocio?» sin contaminar cálculo con fichas simuladas | FR-007/015 |
| Q-019 | Definir reglas de edición/cancelación del movimiento original cuando se muestra en «Mis gastos»; ficha no actúa como operación | FR-009/013 |


**Control de cambios:** toda modificación de una decisión aprobada debe indicar motivo, efectos sobre FR/DR/BR, arquitectura/release/backlog y quién aprueba; documentar formalmente en `DECISIONS.md` cuando se adopte.

## 14. Excelencia y reconocimiento externo

**Requisito metodológico de Software Spec & Delivery v1.3; aún NO completado para Renza.**

- **Qué distinguir:** excelencia UX/interacción vs calidad técnica/seguridad vs validez funcional contable-fiscal vs resultados reales para el cliente.
- **Vías candidatas a investigar según el marco:** The SaaS Awards, iF DESIGN AWARD / Webby Awards y eventualmente FinTech Breakthrough. Son ejemplos **no verificados aquí**: no se declara elegibilidad, edición vigente, costos ni mérito.
- **Próximo trabajo:** seleccionar una vía relevante, verificar rúbrica oficial y edición vigente, traducir criterios aplicables a FR/NFR con aceptación/evidencia; evaluar impacto en accesibilidad, presupuesto y enfoque antes de aprobar el Spec del release.
- **No comprometer candidatura ni convertir premio en criterio de aceptación del software.**

---

## Cierre de MM-PROD-07 y próximo micro-milestone

**MM-PROD-07 — Consolidación documental:** COMPLETADO como borrador de revisión. Las decisiones de dirección `MM-PROD-01` a `MM-PROD-06` se reflejan sin autorizar desarrollo.

**Estado formal del Spec:** `DRAFT / IN_REVIEW`. No hay release aprobado, FR declarados `READY`, ni resultados reales de validación con clientes. El `RELEASE_PLAN.md`, `ARCHITECTURE.md`, `BACKLOG.md` y `DECISIONS.md` canónicos aún deben revisarse/crearse coordinadamente con Product Delivery; este borrador no simula su existencia.

**MM-PROD-08 — Revisión de release candidato y bloqueos decisivos (PROPUESTO)**

- **OBJETIVO:** seleccionar el primer recorrido completo capaz de entregar valor a un usuario real, distinguiendo qué FR entran en v0.1 y qué funciones aprobadas del producto se diferirán; confirmar viabilidad de «Mis costos» con el baseline real.
- **INPUT:** este Spec, auditoría real `MM-ALIGN-02` del front, marco v1.3 y estimación técnica focalizada.
- **INCLUYE:** alcance candidato y exclusiones del primer release, dependencias funcionales más críticas (`Q-001` a `Q-019` **solamente cuando sean bloqueantes**), revisión del estándar externo de excelencia exigido por el marco antes de aprobar release.
- **NO INCLUYE:** implementar código, construir ERP, resolver tax/accounting engine ni generar 100 tickets.
- **DONE CUANDO:** release propuesto y bloqueos identificados por ID, listos para validación/arquitectura y aprobación de dirección.
- **SIGUIENTE:** `ARCHITECTURE.md` contra ese alcance; `RELEASE_PLAN.md` y backlog READY sólo tras el cierre de sus dependencias.

**Pregunta prioritaria de dirección:** ¿la primera entrega a usuarios reales debe incluir la calculadora sencilla y A+ o podemos escalonarlas manteniendo ambas dentro de Renza Free? **Aún no se ha decidido.**

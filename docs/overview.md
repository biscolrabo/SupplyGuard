# SupplyGuard: objetivo del proyecto

## Qué es SupplyGuard

SupplyGuard es una aplicación web para **gestionar los problemas de calidad de las piezas que una fábrica compra a sus proveedores**. Es un proyecto personal de portfolio, inspirado en cómo trabaja el departamento de calidad de recepción (*incoming*) en una planta industrial.

## El problema

Una fábrica, por ejemplo de automóviles, no fabrica todas sus piezas. Muchas las compra a proveedores externos: soportes, tornillos, piezas de plástico, cables… Cuando esas piezas llegan, a veces vienen con defectos, como agujeros mal colocados, medidas fuera de tolerancia, golpes, óxido o materiales incorrectos.

En muchas empresas estos problemas se siguen gestionando con hojas de Excel, correos y papeles. Eso trae varios problemas:

- **La información se dispersa.** Cada persona apunta las cosas a su manera y en sitios distintos.
- **No se sabe en qué punto está cada problema.** ¿Alguien lo está revisando? ¿Se ha hablado con el proveedor? ¿Está resuelto?
- **No queda un historial fiable** de quién hizo qué y cuándo, algo que se pide mucho en las auditorías de calidad.
- **Cuesta ver la foto completa.** Es difícil responder a preguntas como "¿qué proveedor nos da más problemas?" o "¿cuánto tardamos de media en resolver una incidencia?".

## Qué aporta la aplicación

SupplyGuard centraliza todo el proceso en un único sitio, desde que se detecta el defecto hasta que se cierra:

1. **Registro.** Un operario detecta un lote defectuoso y lo registra con la pieza, el lote, el proveedor, la gravedad, una descripción y una foto.
2. **Análisis.** Un ingeniero de calidad revisa la incidencia y busca la causa.
3. **Plan de acción.** El ingeniero define tareas concretas para solucionarlo, cada una con un responsable y una fecha límite.
4. **Cierre.** Cuando todas las tareas se completan, la incidencia se cierra.

Cada paso queda guardado en un **historial**. Además, cada incidencia se podrá descargar como **ficha en PDF** y se enviarán **avisos automáticos** a canales como Teams o Discord.

## Quién la usa

Hay tres tipos de usuario y cada uno solo puede hacer lo que le corresponde:

- **Operario:** registra incidencias y las consulta.
- **Ingeniero:** analiza las incidencias, crea los planes de acción y cambia su estado.
- **Administrador:** gestiona los usuarios, los proveedores y el catálogo de piezas.

## Qué información da

Incluye un panel de indicadores para que los responsables tomen decisiones con datos:

- Cuántas incidencias hay abiertas.
- Cuánto se tarda de media en cerrarlas.
- Un ranking de proveedores según el número de incidencias, que sirve para saber con cuáles hay que hablar o si conviene buscar alternativas.

Más adelante, estos datos se exportarán a una plataforma de análisis en la nube (BigQuery y Looker Studio) para hacer informes más avanzados.

## Por qué este proyecto

Además de resolver un problema real, el proyecto sirve para practicar las tecnologías que se usan en la **digitalización industrial**: APIs, bases de datos, control de accesos por roles, paneles de indicadores, alertas y análisis en la nube.

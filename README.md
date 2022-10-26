# **Parcial 3 Tópicos Avanzados en Bases de Datos**

Aplicación web para el parcial 3 de la materia Tópicos Avanzados en Bases de Datos 2022-2.

Para esta entrega se requería realizar lo siguiente:
* Una Base de Datos embebida con el motor SQLite, en la cual se pudieran realizar operaciones de tipo CRUD (Create, Read, Update y Delete) sobre la BD.
* El dominio del problema debía ser "Pescas Aunap", este debía estar normalizado bajo la forma 2NF.
* Se debía controlar la integridad referencial entre las tablas, como SQLite es un motor con funcionalidades limitadas, este control de la integridad referencial debíamos hacerlo por medio de código.

[Requisitos aplicación](#requisitos-aplicación)

[¿Cómo ejecutar la aplicación?](#cómo-ejecutar-la-aplicación)

[Dominio del problema](#dominio-del-problema)

[Implementación](#implementación)

[Recomendaciones](#recomendaciones)

---

## **Requisitos aplicación**
Para esta sección habrían como dos opciones de requisitos:
* **Si solamente se desea ejecutar la aplicación:**
  
    Para esta opción lo único que se necesita tener descargado en el equipo es Google Chrome, la carpeta del ejecutable y que tu sistema operativo Windows sea de 64 bits.

* **Si se desea entrar el código y no correrla desde el ejecutable**

    Para esta opción habría que tener algunas dependencias descargadas, las cuales son:
    * Python (Versión superior a la 3.10.1 e inferior a la 3.11.0)
    * Librería 'eel'
    * Google Chrome
    * Realizar pull a este repositorio

---

## **¿Cómo ejecutar la aplicación?**

Como fue mencionado anteriormente, se tendrían dos opciones, la primera es por medio de el ejecutable y la segunda sería desde tu instalación local de Python.

### **Desde el ejecutable (forma fácil)**

Esta es la forma sencilla, en este repositorio hay una carpeta que se llama "dist", en esa carpeta habrán 3 archivos los cuales necesitarás descargar localmente en tu dispositivo.

Uno es el ejecutable, otro es la base de datos y el otro es un archivo de texto con el registro de cambios sobre la base de datos.

Una vez tengas descargada esta carpeta con estos 3 archivos, simplemente dale doble clic al archivo .exe y se comenzará a ejecutar el programa (es recomendable que no tengas ninguna ventana de Google Chrome abierta previamente, esto es para que la aplicación se ejecute desde el inicio en modo de pantalla completa).

### **Desde tu intéprete de Python**

Para ejecutarlo desde acá primero debes de instalar los [requisitos previos]() que fueron mencionados anteriormente, una vez tengas todo preparado, te debes situar en la carpeta donde descargaste el repo y ejecutar el comando:

    python main.py

Lo cual comenzará con la ejecución del programa.

---

## **Dominio del Problema**

El dominio del problema que fue planteado es "Pescas AUNAP", este es un dominio ficticio en el que se nos plantea que la AUNAP está interesada en identificar las tendencias actuales en el manejo de la pesca artesanal en las principales cuencas hidrográficas del país. 

Esto se compone en 3 tablas: Pescas, Cuencas Hidrográficas y Métodos de Pesca.

La tabla Pescas es la tabla principal, y las tablas Cuencas y Métodos son tablas secundarias que son usadas en la tabla principal. A continuación se mostrará el esquema relacional de las tablas con sus campos:

---

## **Implementación**

La aplicación fue realizada con la librería de python [eel](https://github.com/python-eel/Eel), esta librería permite realizar aplicaciones tipo "electron" (las cuales son básicamente aplicaciones locales pero con su interfaz gráfica realizada con HTML, CSS y JS), pero en vez de tener el backend con JavaScript, se realizaría con Python. 

La "arquitectura" del programa sería de la siguiente forma:

* El Front-end es realizado con HTML, CSS y JS; lo que sería toda la interfáz, botones, captura de datos, etc...
* El Back-end es realizado con Python; la conexión, consultas y operaciones a la Base de Datos, y la valicación de los datos ingresados en el Front-end.
* El "puente" entre el Front-end y el Back-end tambien sería JS, ya que Python le envía los resultados de las consultas al JS y luego este lo plasma en el Front-end.

En Python realmente solo se usa un script **(main.py)**, la cual contiene los distintos métodos para operaciones y validaciones.

Pero en JavaScript opté por separar las funciones en dos distintas, **functions.js** tiene las funciones de Front-end que requiere la aplicación, y **crud.js** tiene las funciones que conectan el Front con el Back.

---

## **Recomendaciones**

1. La aplicación no es completamente responsive entonces es recomendable usarla en modo pantalla completa.
2. Hay muchos botones con información y ayuda dentro de la aplicación.
3. Se puede realizar scroll en todas las tablas.
4. No usar versiones muy recientes de Python ya que tienen incompatibilidades con la librería eel.
5. Si se desea usar el ejecutable, validar que se tenga una versión de Windows de 64 bits.
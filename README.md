# Esquema de Imagen Secreta Compartida con Detección de Sombras Falsas

Este programa utiliza Python3.11.

En este repositorio se implmentó una version de "(k,n) secret image sharing scheme capable of cheating detection",
propuesto por Liu, X., Sun, Q., Yang C. disponible en https://jwcn-eurasipjournals.springeropen.com/articles/10.1186/s13638-018-1084-7.

## Instalación

A continuación se detallan los pasos para instalar el proyecto en su máquina local.

1. Verifique que tiene instalado Python3.11:

    ```bash
    python --version
    ```
    Si no tiene instalado Python3.11, puede descargarlo [aquí](https://www.python.org/downloads/).

2. Clonar el repositorio:

    ```bash
    git clone https://github.com/nacho9900/secret-image-sharing-with-cheating-detection
    ```
3. Ingrese al directorio del proyecto:

    ```bash
    cd secret-image-sharing-with-cheating-detection
    ```
4. Crear un entorno virtual:

    - Install virtualenv si no lo tiene instalado:
         ```bash
         pip install virtualenv
      ```
    - Crear el entorno virtual:
        ```bash
        virtualenv venv
        ```
    - Activar el entorno virtual en Linux/Mac:
        ```bash
        source venv/bin/activate
        ```
    - Activar el entorno virtual en Windows:
        ```bash
        .\venv\Scripts\activate
        ```
      
A partir de este punto ya se podrá ejecutar el proyecto.

## Ejectuar el proyecto

El programa posee dos modos de ejecución, recuperación y distribución.

### Argumentos

```shell
uso: ss.py [-h] {d,r} file k directory

Secret Image Sharing CLI

Argumentos:
  {d,r}       Operación a realizar: 'd' para distribuir, 'r' para recuperar
  file        Nombre del archivo, ya sea a distribuir o recuperar
  k           Indicar k del esquema (k,n)
  directory   Directorio de las imágenes portadoras o futuras portadoras

options:
  -h, --help  Muestra este mensaje de ayuda y finaliza
```

### Distribución

Para distribuir una imagen secreta en n imágenes portadoras, se debe ejecutar el siguiente comando:

```bash
python ./src/ss.py d <nombre_archivo> <k> <directorio>
```

### Recuperación

Para recuperar una imagen secreta a partir de k imágenes portadoras, se debe ejecutar el siguiente comando:

```bash
python ./src/ss.py r <nombre_archivo> <k> <directorio>
```
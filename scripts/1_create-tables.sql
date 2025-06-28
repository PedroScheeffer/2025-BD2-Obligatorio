use IC_Grupo3;


CREATE TABLE TIPOELECCION (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(255) NOT NULL
);

CREATE TABLE TIPOCANDIDATO(
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(255) NOT NULL
);

CREATE TABLE TIPOVOTO (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(255) NOT NULL
);

CREATE TABLE ZONA (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    paraje VARCHAR(255),
    ciudad VARCHAR(255),
    departamento VARCHAR(255),
    municipio VARCHAR(255)
);

CREATE TABLE ESTABLECIMIENTO (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(255),
    direccion JSON, -- Direccion en formato JSON, con los campos: calle, numero, entre calles, barrio.
    id_zona INTEGER NOT NULL ,
    FOREIGN KEY (id_zona) REFERENCES ZONA(id) ON DELETE CASCADE
);

CREATE TABLE ELECCION (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,

    fecha DATE NOT NULL,
    id_tipo_eleccion INTEGER NOT NULL ,

    FOREIGN KEY (id_tipo_eleccion) REFERENCES TIPOELECCION(id)
);

CREATE TABLE CIRCUITO(
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    accesibilidad BOOLEAN NOT NULL DEFAULT false,
    id_establecimiento INTEGER NOT NULL,
    id_eleccion INTEGER NOT NULL,

    FOREIGN KEY (id_establecimiento) REFERENCES ESTABLECIMIENTO(id) ON DELETE CASCADE,
    FOREIGN KEY (id_eleccion) REFERENCES ELECCION(id) ON DELETE CASCADE
);

-- Personas y tipos 
CREATE TABLE PERSONA(
    -- La credencial civica esta compuesta por 3 letras y numeros ordenados, por ahora 5, ademas de una espacio entre ellas
    cc VARCHAR(15) NOT NULL PRIMARY KEY,

    ci VARCHAR(8) NOT NULL UNIQUE CHECK (ci REGEXP '^[0-9]+$'),
    nombre VARCHAR(255),
    fecha_nacimiento DATE NOT NULL
    contrasena TEXT NOT NULL, -- Por defecto 1234
);

CREATE TABLE VOTANTE(
    cc_persona VARCHAR(15) NOT NULL PRIMARY KEY,

    voto BOOLEAN NOT NULL DEFAULT false,
    id_circuito INTEGER NOT NULL,

    FOREIGN KEY (cc_persona) REFERENCES PERSONA(cc) ON DELETE CASCADE,
    FOREIGN KEY (id_circuito) REFERENCES CIRCUITO(id)
);

CREATE TABLE POLICIA(
    cc_persona VARCHAR(15) NOT NULL PRIMARY KEY,

    comisaria TEXT NOT NULL,
    fk_id_establecimiento INTEGER NOT NULL,
    FOREIGN KEY (cc_persona) REFERENCES PERSONA(cc) ON DELETE CASCADE,
    FOREIGN KEY (fk_id_establecimiento ) REFERENCES ESTABLECIMIENTO(id) ON DELETE CASCADE
);

-- Funcionarios de mesa

CREATE TABLE FUNCIONARIO (
     cc_persona VARCHAR(15) NOT NULL PRIMARY KEY,
    FOREIGN KEY (cc_persona) REFERENCES PERSONA(cc) ON DELETE CASCADE
);

CREATE TABLE PRESIDENTE (
     cc_persona VARCHAR(15) NOT NULL PRIMARY KEY,
    FOREIGN KEY (cc_persona) REFERENCES FUNCIONARIO(cc_persona) ON DELETE CASCADE
);

CREATE TABLE SECRETARIO (
     cc_persona VARCHAR(15) NOT NULL PRIMARY KEY,
    FOREIGN KEY (cc_persona) REFERENCES FUNCIONARIO(cc_persona) ON DELETE CASCADE
);

CREATE TABLE VOCAL (
    cc_persona VARCHAR(15) NOT NULL PRIMARY KEY,
    FOREIGN KEY (cc_persona) REFERENCES FUNCIONARIO(cc_persona) ON DELETE CASCADE
);



CREATE TABLE CANDIDATO (
    cc_persona VARCHAR(15) NOT NULL PRIMARY KEY,
    id_tipo INTEGER NOT NULL,

    FOREIGN KEY (cc_persona) REFERENCES PERSONA(cc) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo) REFERENCES TIPOCANDIDATO(id)
);


CREATE TABLE MESA (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    id_circuito INTEGER NOT NULL,
    cc_vocal VARCHAR(15) NOT NULL,
    cc_secretario VARCHAR(15) NOT NULL,
    cc_presidente VARCHAR(15) NOT NULL,

    FOREIGN KEY (id_circuito) REFERENCES CIRCUITO(id) ON DELETE CASCADE,
    FOREIGN KEY (cc_vocal) REFERENCES VOCAL(cc_persona),
    FOREIGN KEY (cc_secretario) REFERENCES SECRETARIO(cc_persona),
    FOREIGN KEY (cc_presidente) REFERENCES PRESIDENTE(cc_persona)
);

CREATE TABLE PARTIDO (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    direccion_sede JSON NOT NULL
);



CREATE TABLE LISTA (
    valor INTEGER NOT NULL,
    id_partido INTEGER NOT NULL,
    id_eleccion INTEGER NOT NULL,

    PRIMARY KEY (valor, id_partido, id_eleccion),

    FOREIGN KEY (id_partido) REFERENCES PARTIDO(id) ON DELETE CASCADE,
    FOREIGN KEY (id_eleccion) REFERENCES ELECCION(id) ON DELETE CASCADE
);


CREATE TABLE VOTO (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    valor_lista INTEGER NOT NULL,
    id_partido INTEGER NOT NULL,
    id_eleccion INTEGER NOT NULL,
    id_tipo_eleccion INTEGER NOT NULL,
    es_observado BOOLEAN NOT NULL DEFAULT false,
    id_tipo_voto INTEGER NOT NULL,
    id_circuito INTEGER NOT NULL,
    fecha DATE NOT NULL,

    FOREIGN KEY (id_tipo_voto) REFERENCES TIPOVOTO(id),
    FOREIGN KEY (valor_lista, id_partido, id_eleccion) REFERENCES LISTA(valor, id_partido, id_eleccion),
    FOREIGN KEY (id_circuito) REFERENCES CIRCUITO(id)
);

CREATE TABLE CANDIDATO_LISTA(
    cc_persona VARCHAR(15) NOT NULL,
    valor_lista INTEGER NOT NULL,
    id_partido INTEGER NOT NULL,
    id_eleccion INTEGER NOT NULL,

    PRIMARY KEY (cc_persona, valor_lista, id_partido, id_eleccion),
    FOREIGN KEY (cc_persona) REFERENCES PERSONA(cc),
    FOREIGN KEY (valor_lista, id_partido, id_eleccion) REFERENCES LISTA(valor, id_partido, id_eleccion)
);
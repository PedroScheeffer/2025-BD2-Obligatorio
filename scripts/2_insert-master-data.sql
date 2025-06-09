USE IC_Grupo3;

-- First, insert TIPOELECCION data
INSERT INTO TIPOELECCION (tipo) VALUES
('Nacional'),
('Departamental'),
('Municipal');

-- Then insert ZONA data
INSERT INTO ZONA (paraje, ciudad, departamento, municipio) VALUES
('Centro', 'Montevideo', 'Montevideo', 'Montevideo'),
('Pocitos', 'Montevideo', 'Montevideo', 'Montevideo'),
('Malvin', 'Montevideo', 'Montevideo', 'Montevideo');

-- Then ESTABLECIMIENTO data
INSERT INTO ESTABLECIMIENTO (tipo, direccion, id_zona) VALUES
('Escuela', '{"calle": "Calle 123", "numero": 123, "barrio": "Centro"}', 1),
('Centro Comunitario', '{"calle": "Avenida 456", "numero": 456, "barrio": "Sur"}', 2),
('Colegio', '{"calle": "Boulevard 789", "numero": 789, "barrio": "Norte"}', 3);

-- Then ELECCION data (note we reference TIPOELECCION)
INSERT INTO ELECCION (fecha, id_tipo_eleccion) VALUES
('2023-11-05', 1),
('2023-11-19', 2),
('2024-03-10', 3);

-- Now we can insert CIRCUITO data
INSERT INTO CIRCUITO (accesibilidad, id_establecimiento, id_zona, id_eleccion, id_tipo_eleccion) VALUES
(true, 1, 1, 1, 1),
(false, 2, 2, 1, 1),
(true, 3, 3, 1, 1);

-- Insert master data into the database
INSERT INTO TIPOCANDIDATO (descripcion) VALUES
('presidente'),
('vicepresidente'),
('senador'),
('alcalde');

INSERT INTO TIPOELECCION (tipo) VALUES
('presidencial'),
('ballotage'),
('municipales'),
('plebiscito'),
('referéndum');

INSERT INTO TIPOVOTO(tipo) VALUES
('valido'),
('nulo'),
('blanco');


-- TEST DATA 
INSERT INTO ZONA ( paraje, ciudad, departamento, municipio) VALUES
('Paraje A', 'Ciudad X', 'Departamento 1', 'Municipio A'),
('Paraje B', 'Ciudad Y', 'Departamento 2', 'Municipio B'),
('Paraje C', 'Ciudad Z', 'Departamento 3', 'Municipio C');

INSERT INTO ESTABLECIMIENTO (tipo, direccion, id_zona) VALUES
('Escuela', '{"calle": "Calle 123", "numero": 123, "barrio": "Centro"}', 1),
('Centro Comunitario', '{"calle": "Avenida 456", "numero": 456, "barrio": "Sur"}', 2),
('Colegio', '{"calle": "Boulevard 789", "numero": 789, "barrio": "Norte"}', 3);

INSERT INTO CIRCUITO (accesibilidad, id_establecimiento, id_zona, id_eleccion, id_tipo_eleccion) VALUES
(true, 1, 1, 1, 1),
(false, 2, 2, 1, 1),
(false, 3, 3, 1, 1);

INSERT INTO PERSONA (cc, ci, nombre, fecha_nacimiento) VALUES
('ABC 123', '12345678', 'Juan Perez', '1990-01-01'),
('XYZ 456', '87654321', 'Maria Lopez', '1985-05-15'),
('LMN 789', '11223344', 'Carlos Gomez', '2000-10-20');

INSERT INTO VOTANTE (cc_persona, voto, id_circuito) VALUES
('ABC 123', false, 1),
('XYZ 456', false, 2),
('LMN 789', false, 3);

INSERT INTO POLICIA (cc_persona, comisaria, fk_id_establecimiento, fk_id_zona) VALUES
('ABC 123', 'Comisaria Central', 1, 1);

INSERT INTO FUNCIONARIO (cc_persona) VALUES
('XYZ 456'),
('ABC 123'),
('LMN 789');

INSERT INTO SECRETARIO (cc_persona) VALUES
('ABC 123');

INSERT INTO PRESIDENTE (cc_persona) VALUES
('XYZ 456');

INSERT INTO VOCAL (cc_persona) VALUES
('XYZ 456');

INSERT INTO CANDIDATO (cc_persona, id_tipo) VALUES
('LMN 789', 1);

INSERT INTO MESA (id_circuito, cc_vocal, cc_secretario, cc_presidente) VALUES
(1, 'XYZ 456', 'ABC 123', 'XYZ 456');

INSERT INTO ELECCION (fecha, id_tipo_eleccion) VALUES
('2023-11-05', 1),
('2023-11-19', 2),
('2024-03-10', 3);

INSERT INTO PARTIDO (nombre, direccion_sede) VALUES
('Partido A', '{"calle": "Calle Principal", "numero": 100}'),
('Partido B', '{"calle": "Avenida Secundaria", "numero": 200}');

INSERT INTO LISTA (valor, id_partido, id_eleccion, id_tipo_eleccion) VALUES
(1, 1, 1, 1),
(2, 2, 1, 1);

INSERT INTO VOTO (fecha, es_observado, id_tipo_voto, valor_lista, id_partido, id_eleccion, id_tipo_eleccion, id_circuito) VALUES
('2023-11-05', false, 1, 1, 1, 1, 1, 1),
('2023-11-05', true, 2, 2, 2, 1, 1, 2);

INSERT INTO CANDIDATO_LISTA (cc_persona, valor_lista, id_partido, id_eleccion, id_tipo_eleccion) VALUES
('LMN 789', 1, 1, 1, 1),
('ABC 123', 2, 2, 1, 1);


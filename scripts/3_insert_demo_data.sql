-- Demo inserts

USE IC_Grupo3;
-- Commented out master-data inserts; they are defined in 2_insert-master-data.sql
-- INSERT INTO TIPOELECCION (tipo) VALUES ('Presidential'), ('Legislative');
-- INSERT INTO TIPOCANDIDATO (tipo) VALUES ('President'), ('Senator'), ('Representative');
-- INSERT INTO TIPOVOTO (tipo) VALUES ('Normal'), ('Blank'), ('Null');

INSERT INTO ZONA (paraje, ciudad, departamento, municipio) VALUES
  ('Centro', 'Montevideo', 'Montevideo', 'Montevideo'),
  ('Norte', 'Canelones', 'Canelones', 'Canelones');

INSERT INTO ESTABLECIMIENTO (tipo, direccion, id_zona) VALUES
  ('School', '{"calle":"Libertador", "numero":"123", "entre calles":"18 de Julio y Convención", "barrio":"Centro"}', 1),
  ('Community Center', '{"calle":"Sarandí", "numero":"456", "entre calles":"Misiones y Zabala", "barrio":"Barrio Sur"}', 2);

INSERT INTO ELECCION (fecha, id_tipo_eleccion) VALUES
  ('2025-07-04', 1);

INSERT INTO CIRCUITO (accesibilidad, id_establecimiento, id_eleccion) VALUES
  (false, 1, 1),
  (true, 2, 1),
  (false, 1, 1);

INSERT INTO PERSONA (cc, ci, nombre, fecha_nacimiento, contrasena) VALUES
  ('ABC 001', '10000001', 'Juan Perez', '1980-05-20', '1234'),
  ('DEF 002', '10000002', 'Maria Lopez', '1990-08-15', '1234'),
  ('GHI 003', '10000003', 'Carlos Gomez', '1975-12-10', '1234'),
  ('JKL 004', '10000004', 'Ana Martinez', '1985-03-05', '1234'),
  ('MNO 005', '10000005', 'Luis Rodriguez', '1978-11-22', '1234'),
  ('PQR 006', '10000006', 'Elena Fernandez', '1992-07-30', '1234'),
  ('STU 007', '10000007', 'Pedro Alvarez', '1983-02-18', '1234'),
  ('VWX 008', '10000008', 'Laura Garcia', '1988-09-09', '1234'),
  ('YZA 009', '10000009', 'Miguel Torres', '1979-01-12', '1234'),
  ('RES 010', '10000010', 'Persona 10', '1990-01-10', '1234'),
  ('SEC 011', '10000011', 'Persona 11', '1991-02-11', '1234'),
  ('VOC 012', '10000012', 'Persona 12', '1992-03-12', '1234'),
  ('RSP 013', '10000013', 'Persona 13', '1993-04-13', '1234'),
  ('SND 014', '10000014', 'Persona 14', '1994-05-14', '1234'),
  ('VCL 015', '10000015', 'Persona 15', '1995-06-15', '1234'),
  ('XYZ 016', '10000016', 'Persona 16', '1996-07-16', '1234'),
  ('YYY 017', '10000017', 'Persona 17', '1997-08-17', '1234'),
  ('XXX 018', '10000018', 'Persona 18', '1998-09-18', '1234'),
  ('WWW 019', '10000019', 'Persona 19', '1999-10-19', '1234'),
  ('VVV 020', '10000020', 'Persona 20', '2000-11-20', '1234');

INSERT INTO VOTANTE (cc, voto, id_circuito) VALUES
  ('ABC 001', false, 1),
  ('DEF 002', false, 1),
  ('GHI 003', false, 2);

INSERT INTO POLICIA (cc, comisaria, fk_id_establecimiento) VALUES
  ('GHI 003', 'Central', 1);

INSERT INTO FUNCIONARIO (cc) VALUES
  ('JKL 004'),
  ('MNO 005'),
  ('PQR 006'),
  ('STU 007'),
  ('RES 010'),
  ('SEC 011'),
  ('VOC 012'),
  ('RSP 013'),
  ('SND 014'),
  ('VCL 015');

INSERT INTO PRESIDENTE (cc) VALUES ('JKL 004');
INSERT INTO SECRETARIO (cc) VALUES ('MNO 005');
INSERT INTO VOCAL (cc) VALUES ('PQR 006');
INSERT INTO PRESIDENTE (cc) VALUES ('RES 010');
INSERT INTO SECRETARIO (cc) VALUES ('SEC 011');
INSERT INTO VOCAL (cc) VALUES ('VOC 012');
INSERT INTO PRESIDENTE (cc) VALUES ('RSP 013');
INSERT INTO SECRETARIO (cc) VALUES ('SND 014');
INSERT INTO VOCAL (cc) VALUES ('VCL 015');

INSERT INTO CANDIDATO (cc, id_tipo) VALUES
  ('VWX 008', 1),
  ('YZA 009', 2);

INSERT INTO MESA (id_circuito, cc_vocal, cc_secretario, cc_presidente) VALUES
  (1, 'PQR 006', 'MNO 005', 'JKL 004'),
  (2, 'VOC 012', 'SEC 011', 'RES 010'),
  (3, 'VCL 015', 'SND 014', 'RSP 013');

INSERT INTO PARTIDO (nombre, direccion_sede) VALUES
  ('Partido A', '{"calle":"Gonzalo Ramirez", "numero":"789", "entre calles":"Rambla y Gil", "barrio":"Pocitos"}'),
  ('Partido B', '{"calle":"Luis Alberto de Herrera", "numero":"321", "entre calles":"18 de Julio y Bvar España", "barrio":"Centro"}');

INSERT INTO LISTA (valor, id_partido, id_eleccion) VALUES
  (1, 1, 1),
  (2, 2, 1),
  (1, 1, 1);

INSERT INTO VOTO (valor_lista, id_partido, id_eleccion, id_tipo_eleccion, es_observado, id_tipo_voto, id_circuito, fecha) VALUES
  (1, 1, 1, 1, false, 1, 1, '2025-11-02'),
  (2, 2, 1, 1, false, 1, 2, '2025-11-02'),
  (1, 1, 1, 2, false, 1, 3, '2025-09-15');

INSERT INTO CANDIDATO_LISTA (cc, valor_lista, id_partido, id_eleccion) VALUES
  ('VWX 008', 1, 1, 1),
  ('YZA 009', 2, 2, 1);
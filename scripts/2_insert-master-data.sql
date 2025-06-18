USE IC_Grupo3;

-- Insert master data into the database
INSERT INTO TIPOCANDIDATO (tipo) VALUES
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
('anulado'),
('blanco');


BEGIN;

ALTER TABLE mascotas
    ADD COLUMN IF NOT EXISTS especie VARCHAR;

UPDATE mascotas
SET especie = 'No especificada'
WHERE especie IS NULL;

ALTER TABLE mascotas
    ALTER COLUMN especie SET DEFAULT 'No especificada';

ALTER TABLE mascotas
    ALTER COLUMN especie SET NOT NULL;

CREATE INDEX IF NOT EXISTS ix_mascotas_especie
    ON mascotas (especie);

COMMIT;

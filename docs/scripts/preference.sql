BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "preference" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	"default"	BOOLEAN,
	"timestamp"	DATETIME,
	UNIQUE("name"),
	PRIMARY KEY("id")
);
INSERT INTO "preference" VALUES (1,'Fastest',0,'2021-12-29 09:02:09.026049');
INSERT INTO "preference" VALUES (2,'Shortest',1,'2021-12-29 09:02:09.065046');
INSERT INTO "preference" VALUES (3,'Recommended',0,'2021-12-29 09:02:09.070049');
CREATE INDEX IF NOT EXISTS "ix_preference_default" ON "preference" (
	"default"
);
COMMIT;

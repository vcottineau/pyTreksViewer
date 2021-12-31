BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "folder" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	"timestamp"	DATETIME,
	UNIQUE("name"),
	PRIMARY KEY("id")
);
INSERT INTO "folder" VALUES (1,'France','2021-12-30 14:12:57');
COMMIT;

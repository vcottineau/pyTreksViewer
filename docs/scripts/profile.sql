BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "profile" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	"default"	BOOLEAN,
	"timestamp"	DATETIME,
	UNIQUE("name"),
	PRIMARY KEY("id")
);
INSERT INTO "profile" VALUES (1,'Driving',0,'2021-12-29 09:02:08.761547');
INSERT INTO "profile" VALUES (2,'Cycling',1,'2021-12-29 09:02:08.786649');
INSERT INTO "profile" VALUES (3,'Walking',0,'2021-12-29 09:02:08.802275');
INSERT INTO "profile" VALUES (4,'Hicking',0,'2021-12-29 09:02:08.802275');
CREATE INDEX IF NOT EXISTS "ix_profile_default" ON "profile" (
	"default"
);
COMMIT;

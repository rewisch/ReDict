CREATE TABLE "Definition" (
	"DefinitionId"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"DictionaryId"	INTEGER,
	"WordId"	INTEGER,
	"Definition"	TEXT
)

GO

CREATE TABLE "Dictionary" (
	"DictionaryId"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Name"	TEXT NOT NULL,
	"WordCount"	INTEGER NOT NULL,
	"Abstractive"	INTEGER
)

GO

CREATE TABLE "Flection" (
	"FlectionId"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"WordId"	INTEGER NOT NULL,
	"Flection"	TEXT NOT NULL,
	"Description"	TEXT NOT NULL,
	"NoFlection"	INTEGER
)

GO

CREATE TABLE "History" (
	"HistoryId"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"WordId"	INTEGER NOT NULL
)

GO

CREATE TABLE "Property" (
	"PropertyId"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Value"	TEXT NOT NULL,
	"Description"	TEXT
)

GO

CREATE TABLE "Word" (
	"WordId"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"Word"	TEXT NOT NULL UNIQUE
)

GO


CREATE INDEX "Id" ON "Dictionary" (
	"DictionaryId"	ASC
)

GO

CREATE INDEX "idx_definition_wordid" ON "Definition" (
	"WordId"
)

GO

CREATE INDEX "idx_flection_flection" ON "Flection" (
	"Flection"	ASC,
	"FlectionId"	ASC
)

GO

CREATE UNIQUE INDEX "idx_word_word" ON "Word" (
	"Word"	ASC,
	"WordId"	ASC
)

GO
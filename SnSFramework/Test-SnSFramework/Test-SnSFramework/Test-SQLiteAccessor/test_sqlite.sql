CREATE TABLE TableA(
	tid				INTEGER UNIQUE NOT NULL,
 	vchar			VARCHAR(10) NOT NULL DEFAULT '',
 	integ			INTEGER NOT NULL DEFAULT 0,
 	PRIMARY KEY (tid)
);
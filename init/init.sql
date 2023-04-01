CREATE DATABASE kartaca;

USE kartaca;

CREATE TABLE country (
  id INT NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  continent VARCHAR(255)
);

CREATE TABLE currency (
  id INT NOT NULL PRIMARY KEY,
  code CHAR(3) NOT NULL,
  name VARCHAR(255)
);

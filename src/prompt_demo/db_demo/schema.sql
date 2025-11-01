CREATE TABLE orders (
    id integer NOT NULL,
    client_id integer,
    product_id integer,
    quantity integer,
    "timestamp" timestamp without time zone
);

CREATE TABLE clients (
    id integer NOT NULL,
    name character varying,
    email character varying,
    location character varying
);

CREATE TABLE orders (
    id integer NOT NULL,
    client_id integer,
    product_id integer,
    quantity integer,
    "timestamp" timestamp without time zone
);

ALTER TABLE ONLY clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (id);

ALTER TABLE ONLY orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);

ALTER TABLE ONLY products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);

ALTER TABLE ONLY orders
    ADD CONSTRAINT orders_client_id_fkey FOREIGN KEY (client_id) REFERENCES clients(id);

ALTER TABLE ONLY orders
    ADD CONSTRAINT orders_product_id_fkey FOREIGN KEY (product_id) REFERENCES products(id);


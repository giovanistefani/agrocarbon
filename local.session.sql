CREATE TABLE agrocarbon.propriedade_produtor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    propriedade_id INT NOT NULL,
    produtor_id INT NOT NULL,
    FOREIGN KEY (propriedade_id) REFERENCES propriedades(id),
    FOREIGN KEY (produtor_id) REFERENCES produtores(id)
);
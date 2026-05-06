
-- Base de datos: biblioteca
-- Proyecto SENA ADSO - Microservicios

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
SET NAMES utf8mb4;

-- Estructura de tabla: paises
CREATE TABLE IF NOT EXISTS `paises` (
  `idPais` varchar(2) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `continente` varchar(15) NOT NULL,
  PRIMARY KEY (`idPais`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Datos de ejemplo para paises
INSERT IGNORE INTO `paises` (`idPais`, `nombre`, `continente`) VALUES
('AR', 'Argentina',        'America'),
('BR', 'Brasil',           'America'),
('CO', 'Colombia',         'America'),
('DE', 'Alemania',         'Europa'),
('ES', 'España',           'Europa'),
('FR', 'Francia',          'Europa'),
('GB', 'Reino Unido',      'Europa'),
('MX', 'México',           'America'),
('US', 'Estados Unidos',   'America');

-- Estructura de tabla: autores
CREATE TABLE IF NOT EXISTS `autores` (
  `idAutor` varchar(10) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `idPais` varchar(2) NOT NULL,
  PRIMARY KEY (`idAutor`),
  KEY `idPais` (`idPais`),
  CONSTRAINT `autores_ibfk_1` FOREIGN KEY (`idPais`) REFERENCES `paises` (`idPais`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Datos de ejemplo para autores
INSERT IGNORE INTO `autores` (`idAutor`, `nombre`, `email`, `idPais`) VALUES
('AU001', 'Gabriel García Márquez', 'garcia@literatura.com', 'CO'),
('AU002', 'Jorge Luis Borges',      'borges@letras.com',     'AR'),
('AU003', 'Isabel Allende',         'allende@letras.com',    'CO'),
('AU004', 'Mario Vargas Llosa',     'vargas@letras.com',     'ES'),
('AU005', 'Julio Cortázar',         'cortazar@letras.com',   'AR');

-- Estructura de tabla: editoriales
CREATE TABLE IF NOT EXISTS `editoriales` (
  `idEditorial` varchar(5) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `idPais` varchar(2) NOT NULL,
  PRIMARY KEY (`idEditorial`),
  KEY `idPais` (`idPais`),
  CONSTRAINT `editoriales_ibfk_1` FOREIGN KEY (`idPais`) REFERENCES `paises` (`idPais`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Datos de ejemplo para editoriales
INSERT IGNORE INTO `editoriales` (`idEditorial`, `nombre`, `idPais`) VALUES
('ED001', 'Alfaguara',         'ES'),
('ED002', 'Planeta',           'ES'),
('ED003', 'Norma',             'CO'),
('ED004', 'Penguin Random',    'US'),
('ED005', 'Seix Barral',       'ES');

-- Estructura de tabla: lectores
CREATE TABLE IF NOT EXISTS `lectores` (
  `idLector` varchar(10) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `cupoLibros` int(11) NOT NULL,
  `cupoPrestados` int(11) NOT NULL,
  `enMora` tinyint(1) NOT NULL,
  PRIMARY KEY (`idLector`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Datos de ejemplo para lectores
INSERT IGNORE INTO `lectores` (`idLector`, `nombre`, `cupoLibros`, `cupoPrestados`, `enMora`) VALUES
('LEC001', 'Ana Gomez',      5, 2, 0),
('LEC002', 'Pedro Ramirez',  3, 3, 1),
('LEC003', 'Sofia Torres',   5, 0, 0);

-- Estructura de tabla: libros
CREATE TABLE IF NOT EXISTS `libros` (
  `idLibro` varchar(12) NOT NULL,
  `titulo` varchar(50) NOT NULL,
  `idioma` varchar(10) NOT NULL,
  `idAutor` varchar(10) NOT NULL,
  `idEditorial` varchar(5) NOT NULL,
  `numeroEjemplares` int(11) NOT NULL,
  `ejemplaresPrestados` int(11) NOT NULL,
  PRIMARY KEY (`idLibro`),
  KEY `idAutor` (`idAutor`),
  KEY `idEditorial` (`idEditorial`),
  CONSTRAINT `libros_ibfk_1` FOREIGN KEY (`idAutor`) REFERENCES `autores` (`idAutor`),
  CONSTRAINT `libros_ibfk_2` FOREIGN KEY (`idEditorial`) REFERENCES `editoriales` (`idEditorial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Datos de ejemplo para libros
INSERT IGNORE INTO `libros` (`idLibro`, `titulo`, `idioma`, `idAutor`, `idEditorial`, `numeroEjemplares`, `ejemplaresPrestados`) VALUES
('LIB001', 'Cien años de soledad',      'Español', 'AU001', 'ED003', 10, 2),
('LIB002', 'El amor en los tiempos',    'Español', 'AU001', 'ED001', 8,  1),
('LIB003', 'Ficciones',                 'Español', 'AU002', 'ED002', 6,  0),
('LIB004', 'La casa de los espíritus',  'Español', 'AU003', 'ED001', 7,  3),
('LIB005', 'Rayuela',                   'Español', 'AU005', 'ED005', 5,  0);

-- 
-- Estructura de tabla: prestamos
-- 
CREATE TABLE IF NOT EXISTS `prestamos` (
  `idPrestamo` int(11) NOT NULL AUTO_INCREMENT,
  `idLibro` varchar(12) NOT NULL,
  `idLector` varchar(10) NOT NULL,
  `fechaPrestamo` date NOT NULL,
  `fechaPropuestaDev` date NOT NULL,
  `fechaRealDev` date NOT NULL,
  PRIMARY KEY (`idPrestamo`),
  KEY `fk_idLibro` (`idLibro`),
  KEY `fk_idLector` (`idLector`),
  CONSTRAINT `fk_idLector` FOREIGN KEY (`idLector`) REFERENCES `lectores` (`idLector`),
  CONSTRAINT `fk_idLibro`  FOREIGN KEY (`idLibro`)  REFERENCES `libros` (`idLibro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Datos de ejemplo para prestamos
INSERT IGNORE INTO `prestamos` (`idLibro`, `idLector`, `fechaPrestamo`, `fechaPropuestaDev`, `fechaRealDev`) VALUES
('LIB001', 'LEC001', '2026-04-01', '2026-04-15', '2026-04-14'),
('LIB004', 'LEC002', '2026-04-05', '2026-04-19', '0000-00-00');

-- Estructura de tabla: usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `idUsuario` varchar(15) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `contrasena` varchar(128) NOT NULL,
  PRIMARY KEY (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Datos de ejemplo para usuarios
INSERT IGNORE INTO `usuarios` (`idUsuario`, `nombre`, `contrasena`) VALUES
('afvelasco',      'Andrés Fernando Velasco', 'd404559f602eab6fd602ac7680dacbfaadd13630335e951f097af3900e9de176b6db28512f2e000b9d04fba5133e8b1c6e8df59db3a8ab9d60be4b97cc9e81db'),
('danielguapo',    'Daniel el Guapo',         '4444'),
('joseysamuel',    'Jose y Samuel',            '9876'),
('posadita',       'Kevin Posada',             '3114251'),
('santiagocaiced', 'Santiago Caicedo',         '0000');

COMMIT;

-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 08-01-2018 a las 22:19:29
-- Versión del servidor: 10.1.29-MariaDB
-- Versión de PHP: 7.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `eoi2`
--
CREATE DATABASE IF NOT EXISTS `eoi2` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `eoi2`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

DROP TABLE IF EXISTS `categorias`;
CREATE TABLE IF NOT EXISTS `categorias` (
  `categoria` int(11) NOT NULL,
  `titulo` varchar(100) DEFAULT NULL,
  `salario` int(11) DEFAULT NULL,
  `trienio` int(11) DEFAULT NULL,
  PRIMARY KEY (`categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`categoria`, `titulo`, `salario`, `trienio`) VALUES
(1, 'Director', 50000, 1000),
(2, 'Jefe Seccion', 40000, 800),
(3, 'Administrativo', 35000, 700),
(4, 'Comercial', 35000, 700),
(5, 'Empleado de Almacen', 25000, 500);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `departamentos`
--

DROP TABLE IF EXISTS `departamentos`;
CREATE TABLE IF NOT EXISTS `departamentos` (
  `deptno` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`deptno`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `departamentos`
--

INSERT INTO `departamentos` (`deptno`, `nombre`) VALUES
(1, 'Dirección'),
(2, 'Administración'),
(3, 'Comercial'),
(4, 'Almacén'),
(5, 'Informática');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dptoficinas`
--

DROP TABLE IF EXISTS `dptoficinas`;
CREATE TABLE IF NOT EXISTS `dptoficinas` (
  `codigo` int(11) NOT NULL,
  `oficina` int(11) DEFAULT NULL,
  `departamento` int(11) DEFAULT NULL,
  `telefono` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`codigo`),
  KEY `apuntoaoficina` (`oficina`),
  KEY `apuntoadepartamento` (`departamento`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `dptoficinas`
--

INSERT INTO `dptoficinas` (`codigo`, `oficina`, `departamento`, `telefono`) VALUES
(100, 11, 1, '963.981.000'),
(101, 11, 2, '963.981.100'),
(102, 11, 3, '963.981.200'),
(103, 11, 4, '963.981.300'),
(104, 11, 5, '963.981.400'),
(105, 12, 2, '963.551.000'),
(106, 12, 3, '963.551.100'),
(107, 12, 4, '963.551.200'),
(108, 13, 3, '961.671.000'),
(109, 21, 2, '913.641.000'),
(110, 21, 3, '913.641.100'),
(111, 21, 4, '913.641.200'),
(112, 22, 3, '925.871.000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

DROP TABLE IF EXISTS `empleados`;
CREATE TABLE IF NOT EXISTS `empleados` (
  `num` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `edad` int(11) NOT NULL,
  `departamento` int(11) NOT NULL,
  `categoria` int(11) NOT NULL,
  `contrato` date NOT NULL,
  PRIMARY KEY (`num`),
  KEY `tienecategoria` (`categoria`),
  KEY `tienedepartamento` (`departamento`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`num`, `nombre`, `edad`, `departamento`, `categoria`, `contrato`) VALUES
(1000, 'Antonio Gutierrez', 45, 100, 1, '1989-01-12'),
(1001, 'Paloma Blanco', 56, 100, 2, '1992-03-17'),
(1002, 'Antonio Pazos', 52, 100, 3, '1986-03-14'),
(1003, 'Ana Garcia', 27, 101, 2, '1995-10-23'),
(1004, 'Amparo Beltran', 28, 101, 3, '1998-02-04'),
(1005, 'Enrique Gomez', 36, 101, 3, '2000-07-05'),
(1006, 'Nieves Soler', 25, 105, 2, '1996-03-13'),
(1007, 'Juan Jose Velasco', 34, 105, 3, '1997-02-14'),
(1008, 'Isidro Perez', 22, 109, 2, '2000-05-06'),
(1009, 'Ignacio Lopez', 38, 109, 3, '1990-04-07'),
(1010, 'Vicente Salvador', 29, 109, 3, '1995-07-08'),
(1011, 'Carmen Hernandez', 44, 102, 2, '1990-07-16'),
(1012, 'Juan Pons', 50, 102, 4, '1994-04-14'),
(1013, 'Pedro Fernandez', 23, 102, 4, '1999-09-16'),
(1014, 'Silvia Blasco', 33, 102, 4, '1992-02-23'),
(1015, 'Jose Alegre', 26, 106, 2, '1997-08-26'),
(1016, 'Cristina Prats', 46, 106, 4, '1984-11-18'),
(1017, 'Carlos Gimenez', 35, 106, 4, '1995-05-15'),
(1018, 'Maria Gonzalez', 37, 108, 4, '1996-06-16'),
(1019, 'Manuel Torres', 24, 108, 4, '1998-01-19'),
(1020, 'Jose Perez', 28, 110, 2, '1996-03-22'),
(1021, 'Alejandro Martos', 34, 110, 4, '1994-10-17'),
(1022, 'Veronica Muelas', 25, 110, 4, '1997-07-05'),
(1023, 'Elena Lopez', 29, 112, 4, '1994-07-09'),
(1024, 'Isabel Fernandez', 22, 112, 4, '2000-10-12'),
(1025, 'Jose Mujica', 49, 103, 2, '1987-09-04'),
(1026, 'Pedro Bledos', 26, 103, 5, '1998-02-06'),
(1027, 'Pablo Costas', 35, 107, 5, '1995-07-03'),
(1028, 'Ester Castro', 27, 111, 2, '1996-07-18'),
(1029, 'Gregoria Mas', 33, 111, 5, '1997-03-14'),
(1030, 'Jose Medina', 34, 104, 2, '1995-06-14'),
(1031, 'Maria Utrillas', 27, 104, 3, '1997-08-19'),
(1032, 'Marina Gilabert', 24, 104, 3, '1998-12-01');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `oficinas`
--

DROP TABLE IF EXISTS `oficinas`;
CREATE TABLE IF NOT EXISTS `oficinas` (
  `oficina` int(11) NOT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`oficina`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `oficinas`
--

INSERT INTO `oficinas` (`oficina`, `ciudad`, `region`) VALUES
(11, 'Valencia', 'Este'),
(12, 'Barcelona', 'Este'),
(13, 'Alicante', 'Este'),
(21, 'Madrid', 'Centro'),
(22, 'Toledo', 'Centro');

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `dptoficinas`
--
ALTER TABLE `dptoficinas`
  ADD CONSTRAINT `apuntoadepartamento` FOREIGN KEY (`departamento`) REFERENCES `departamentos` (`deptno`) ON DELETE SET NULL,
  ADD CONSTRAINT `apuntoaoficina` FOREIGN KEY (`oficina`) REFERENCES `oficinas` (`oficina`) ON DELETE SET NULL;

--
-- Filtros para la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD CONSTRAINT `tienecategoria` FOREIGN KEY (`categoria`) REFERENCES `categorias` (`categoria`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tienedepartamento` FOREIGN KEY (`departamento`) REFERENCES `dptoficinas` (`codigo`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
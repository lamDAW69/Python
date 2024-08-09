-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-12-2017 a las 08:17:04
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
-- Base de datos: `eoi`
--
CREATE DATABASE IF NOT EXISTS `eoi` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `eoi`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

DROP TABLE IF EXISTS `clientes`;
CREATE TABLE `clientes` (
  `num_clie` int(11) NOT NULL,
  `empresa` varchar(100) NOT NULL,
  `rep_clie` int(11) NOT NULL,
  `limite_credito` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`num_clie`, `empresa`, `rep_clie`, `limite_credito`) VALUES
(2101, 'Exclusivas Soriano S.A.', 106, 65000),
(2102, 'Exclusivas del Este S.L.', 101, 65000),
(2103, 'Pino S.L.', 105, 50000),
(2105, 'MALB S.A.', 101, 45000),
(2106, 'Construcciones Leon S.A.', 102, 65000),
(2107, 'Distribuciones Sur S.A', 110, 35000),
(2108, 'Zapater Importaciones S.A.', 109, 55000),
(2109, 'Roda & Castedo S.L.', 103, 25000),
(2111, 'EVBE S.A.', 103, 50000),
(2112, 'Lopez Asociados S.L.', 108, 50000),
(2113, 'Importaciones Martin S.L.', 104, 20000),
(2114, 'Componentes Fernandez S.A.', 102, 20000),
(2115, 'AFS S.A.', 101, 20000),
(2117, 'Hnos. Ramon S.L.', 106, 35000),
(2118, 'Exclusivas Norte S.A.', 108, 60000),
(2119, 'Martinez & Garcia S.L.', 109, 25000),
(2120, 'Distribuciones Montiel S.L.', 102, 50000),
(2121, 'Hernandez & hijos S.L.', 103, 45000),
(2122, 'JPF S.L.', 105, 30000),
(2123, 'Hnos. Martinez S.A.', 102, 40000),
(2124, 'Domingo S.L.', 107, 40000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `oficinas`
--

DROP TABLE IF EXISTS `oficinas`;
CREATE TABLE `oficinas` (
  `oficina` int(11) NOT NULL,
  `ciudad` varchar(100) NOT NULL,
  `region` varchar(100) NOT NULL,
  `dir` int(11) NOT NULL,
  `objetivo` int(11) NOT NULL,
  `ventas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `oficinas`
--

INSERT INTO `oficinas` (`oficina`, `ciudad`, `region`, `dir`, `objetivo`, `ventas`) VALUES
(11, 'Valencia', 'Este', 106, 52500, 40063),
(12, 'Barcelona', 'Este', 105, 70000, 29328),
(13, 'Alicante', 'Este', 104, 30000, 39327),
(21, 'Madrid', 'Centro', 108, 60000, 81309),
(22, 'Toledo', 'Centro', 108, 27500, 34432);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
CREATE TABLE `pedidos` (
  `num_pedido` int(11) NOT NULL,
  `fecha_pedido` date NOT NULL,
  `clie` int(11) NOT NULL,
  `rep` int(11) NOT NULL,
  `fab` varchar(100) NOT NULL,
  `producto` varchar(100) NOT NULL,
  `cant` int(11) NOT NULL,
  `importe` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`num_pedido`, `fecha_pedido`, `clie`, `rep`, `fab`, `producto`, `cant`, `importe`) VALUES
(110036, '2000-01-30', 2107, 110, 'ACI', '4100Z', 9, 22500),
(112961, '1999-12-17', 2117, 106, 'REI', '2A44L', 7, 31500),
(112963, '1999-12-17', 2103, 105, 'ACI', '41004', 28, 3276),
(112968, '1999-10-12', 2102, 101, 'ACI', '41004', 34, 3978),
(112975, '1999-10-12', 2111, 103, 'REI', '2A44G', 6, 2100),
(112979, '1999-10-12', 2114, 102, 'ACI', '4100Z', 6, 15000),
(112983, '1999-12-27', 2103, 105, 'ACI', '41004', 6, 702),
(112987, '1999-12-31', 2103, 105, 'ACI', '4100Y', 11, 27500),
(112989, '2000-01-03', 2101, 106, 'FEA', '114', 6, 1458),
(112992, '1999-11-04', 2118, 108, 'ACI', '41002', 10, 760),
(112993, '2000-01-04', 2106, 102, 'REI', '2A45C', 24, 1896),
(112997, '2000-01-08', 2124, 107, 'BIC', '41003', 1, 652),
(113003, '2000-01-25', 2108, 109, 'IMM', '779C', 3, 5625),
(113007, '2000-01-08', 2112, 108, 'IMM', '773C', 3, 2825),
(113012, '2000-01-11', 2111, 105, 'ACI', '41003', 35, 3745),
(113013, '2000-01-14', 2118, 108, 'BIC', '41003', 1, 652),
(113024, '2000-01-20', 2114, 108, 'QSA', 'XK47', 20, 7100),
(113027, '2000-02-22', 2103, 105, 'ACI', '41002', 54, 4104),
(113034, '2000-01-29', 2107, 110, 'REI', '2A45C', 8, 632),
(113042, '2000-02-02', 2113, 101, 'REI', '2A44R', 5, 22500),
(113045, '2000-02-02', 2112, 108, 'REI', '2A44R', 10, 45000),
(113048, '2000-02-10', 2120, 102, 'IMM', '779C', 2, 3750),
(113049, '2000-02-10', 2118, 108, 'QSA', 'XK47', 2, 776),
(113051, '2000-02-10', 2118, 108, 'QSA', 'XK47', 4, 1420),
(113055, '2000-02-15', 2108, 101, 'ACI', '4100X', 6, 150),
(113057, '2000-02-18', 2111, 103, 'ACI', '4100X', 24, 600),
(113058, '2000-02-23', 2108, 109, 'FEA', '112', 10, 1480),
(113062, '2000-02-24', 2124, 107, 'FEA', '114', 10, 2430),
(113065, '2000-02-27', 2106, 102, 'QSA', 'XK47', 6, 2130),
(113069, '2000-03-02', 2109, 107, 'IMM', '775C', 22, 31350);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

DROP TABLE IF EXISTS `productos`;
CREATE TABLE `productos` (
  `id_fab` varchar(100) NOT NULL,
  `id_producto` varchar(100) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `precio` int(11) NOT NULL,
  `existencias` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_fab`, `id_producto`, `descripcion`, `precio`, `existencias`) VALUES
('ACI', '41001', 'Articulo Tipo 1', 55, 277),
('ACI', '41002', 'Articulo Tipo 2', 76, 167),
('ACI', '41003', 'Articulo Tipo 3', 107, 207),
('ACI', '41004', 'Articulo Tipo 4', 117, 139),
('ACI', '4100X', 'Ajustador', 25, 37),
('ACI', '4100Y', 'Extractor', 2750, 25),
('ACI', '4100Z', 'Montador', 2500, 28),
('BIC', '41003', 'Manivela', 652, 3),
('BIC', '41089', 'Reten', 225, 78),
('BIC', '41672', 'Plate', 180, 0),
('FEA', '112', 'Cubierta', 148, 115),
('FEA', '114', 'Bancada Motor', 243, 15),
('IMM', '773C', 'Riostra 1/2-Tm', 975, 28),
('IMM', '775C', 'Riostra 1-Tm', 1425, 5),
('IMM', '779C', 'Riostra 2-Tm', 1875, 9),
('IMM', '887H', 'Soporte Riostra', 54, 223),
('IMM', '887P', 'Perno Riostra', 250, 24),
('IMM', '887X', 'Retenedor Riostra', 475, 32),
('QSA', 'XK47', 'Reductor', 355, 38),
('QSA', 'XK48', 'Reductor', 134, 203),
('QSA', 'XK48A', 'Reductor', 117, 37),
('REI', '2A44G', 'Pasador Bisagra', 350, 14),
('REI', '2A44L', 'Bisagra Izqda.', 4500, 12),
('REI', '2A44R', 'Bisagra Derecha', 4500, 12),
('REI', '2A45C', 'V Stago Trinquete', 79, 210);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `repventas`
--

DROP TABLE IF EXISTS `repventas`;
CREATE TABLE `repventas` (
  `num_empl` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `edad` int(11) NOT NULL,
  `oficina_rep` int(11) DEFAULT NULL,
  `titulo` varchar(100) NOT NULL,
  `contrato` date NOT NULL,
  `director` int(11) DEFAULT NULL,
  `cuota` int(11) DEFAULT NULL,
  `ventas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `repventas`
--

INSERT INTO `repventas` (`num_empl`, `nombre`, `edad`, `oficina_rep`, `titulo`, `contrato`, `director`, `cuota`, `ventas`) VALUES
(101, 'Daniel Gutierrez', 45, 12, 'Rept Ventas', '1996-10-20', 104, 27500, 26628),
(102, 'Soledad Martinez', 48, 21, 'Rept Ventas', '1996-12-10', 108, 30000, 22776),
(103, 'Pedro Cruz', 29, 12, 'Rept Ventas', '1997-03-01', 104, 25000, 2700),
(104, 'Carlos Martinez', 33, 12, 'Dir. Ventas', '1997-05-19', 106, 17500, 0),
(105, 'Belen Aguirre', 37, 13, 'Dir. Ventas', '1998-02-12', 104, 30000, 39327),
(106, 'Jose Maldonado', 52, 11, 'VP Ventas', '1998-06-14', NULL, 25000, 32958),
(107, 'Natalia Martin', 49, 22, 'Rept Ventas', '1998-11-14', 108, 27500, 34432),
(108, 'Lorenzo Fernandez', 62, 21, 'Dir. Ventas', '1999-10-12', 106, 30000, 58533),
(109, 'Maria Garcia', 31, 11, 'Rept Ventas', '1999-10-12', 106, 27500, 7105),
(110, 'Antonio Valle', 41, NULL, 'Rept Ventas', '2000-01-13', 101, 0, 23123);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`num_clie`),
  ADD KEY `FK_CLIENTE_REPVENTAS` (`rep_clie`);

--
-- Indices de la tabla `oficinas`
--
ALTER TABLE `oficinas`
  ADD PRIMARY KEY (`oficina`),
  ADD KEY `FK_OFICINAS_REPVENTAS` (`dir`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`num_pedido`),
  ADD KEY `FK_PEDIDOS_PRODUCTOS` (`fab`,`producto`),
  ADD KEY `FK_PEDIDOS_CLIENTE` (`clie`),
  ADD KEY `FK_PEDIDOS_REPVENTAS` (`rep`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_fab`,`id_producto`);

--
-- Indices de la tabla `repventas`
--
ALTER TABLE `repventas`
  ADD PRIMARY KEY (`num_empl`),
  ADD KEY `FK_REPVENTAS_REPVENTAS` (`director`),
  ADD KEY `FK_REPVENTAS_OFICINAS` (`oficina_rep`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `FK_CLIENTE_REPVENTAS` FOREIGN KEY (`rep_clie`) REFERENCES `repventas` (`num_empl`);

--
-- Filtros para la tabla `oficinas`
--
ALTER TABLE `oficinas`
  ADD CONSTRAINT `FK_OFICINAS_REPVENTAS` FOREIGN KEY (`dir`) REFERENCES `repventas` (`num_empl`);

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `FK_PEDIDOS_CLIENTE` FOREIGN KEY (`clie`) REFERENCES `clientes` (`num_clie`),
  ADD CONSTRAINT `FK_PEDIDOS_PRODUCTOS` FOREIGN KEY (`fab`,`producto`) REFERENCES `productos` (`id_fab`, `id_producto`),
  ADD CONSTRAINT `FK_PEDIDOS_REPVENTAS` FOREIGN KEY (`rep`) REFERENCES `repventas` (`num_empl`);

--
-- Filtros para la tabla `repventas`
--
ALTER TABLE `repventas`
  ADD CONSTRAINT `FK_REPVENTAS_OFICINAS` FOREIGN KEY (`oficina_rep`) REFERENCES `oficinas` (`oficina`),
  ADD CONSTRAINT `FK_REPVENTAS_REPVENTAS` FOREIGN KEY (`director`) REFERENCES `repventas` (`num_empl`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
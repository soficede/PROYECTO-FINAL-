-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-12-2024 a las 21:48:13
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestion_medicamentos`
--
CREATE DATABASE IF NOT EXISTS `gestion_medicamentos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `gestion_medicamentos`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alertas`
--

CREATE TABLE `alertas` (
  `id` int(11) NOT NULL,
  `tipo` varchar(255) DEFAULT NULL,
  `mensaje` text DEFAULT NULL,
  `estado` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alertas`
--

INSERT INTO `alertas` (`id`, `tipo`, `mensaje`, `estado`) VALUES
(1, 'Recordatorio', 'Es hora de tomar el medicamento juan.', 1),
(2, 'Recordatorio', 'Es hora de tomar el medicamento segundo.', 0),
(3, 'Vencimiento', 'El medicamento juan ha vencido. Fecha de vencimiento: 2023-12-01', 0),
(4, 'Vencimiento', 'El medicamento juan ha vencido. Fecha de vencimiento: 2023-12-01', 0),
(5, 'Tomar Medicamento', 'Es hora de tomar el medicamento juan. Última toma: 2023-12-01 00:00:00, próxima toma: 2023-12-01 09:00:00', 0),
(6, 'Vencimiento', 'El medicamento segundo ha vencido. Fecha de vencimiento: 1999-01-10', 0),
(7, 'Tomar Medicamento', 'Es hora de tomar el medicamento segundo. Última toma: 1999-01-10 00:00:00, próxima toma: 1999-01-10 21:00:00', 0),
(8, 'Vencimiento', 'El medicamento juan ha vencido. Fecha de vencimiento: 2023-12-01', 0),
(9, 'Vencimiento', 'El medicamento segundo ha vencido. Fecha de vencimiento: 1999-01-10', 0),
(10, 'Vencimiento', 'El medicamento juan ha vencido. Fecha de vencimiento: 2023-12-01', 0),
(11, 'Vencimiento', 'El medicamento segundo ha vencido. Fecha de vencimiento: 1999-01-10', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `medicamentos`
--

CREATE TABLE `medicamentos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `dosis` varchar(255) NOT NULL,
  `frecuencia` varchar(255) NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `stock` int(11) NOT NULL,
  `fecha_ingreso` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `medicamentos`
--

INSERT INTO `medicamentos` (`id`, `nombre`, `dosis`, `frecuencia`, `fecha_vencimiento`, `stock`, `fecha_ingreso`) VALUES
(1, 'juan', '12', '9', '2023-12-01', 12, NULL),
(2, 'segundo', '-12', '21', '1999-01-10', 1, NULL),
(3, 'si', '12', '12', '2024-12-12', 12, NULL),
(4, 'si', '12', '12', '2024-12-12', 0, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seguimiento_medicamentos`
--

CREATE TABLE `seguimiento_medicamentos` (
  `id` int(11) NOT NULL,
  `medicamento_id` int(11) DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_final` date DEFAULT NULL,
  `stock_final` int(11) DEFAULT NULL,
  `frecuencia` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alertas`
--
ALTER TABLE `alertas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `medicamentos`
--
ALTER TABLE `medicamentos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `seguimiento_medicamentos`
--
ALTER TABLE `seguimiento_medicamentos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `medicamento_id` (`medicamento_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alertas`
--
ALTER TABLE `alertas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `medicamentos`
--
ALTER TABLE `medicamentos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `seguimiento_medicamentos`
--
ALTER TABLE `seguimiento_medicamentos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `seguimiento_medicamentos`
--
ALTER TABLE `seguimiento_medicamentos`
  ADD CONSTRAINT `seguimiento_medicamentos_ibfk_1` FOREIGN KEY (`medicamento_id`) REFERENCES `medicamentos` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

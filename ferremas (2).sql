-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 15-07-2024 a las 01:59:16
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ferremas`
--
CREATE DATABASE IF NOT EXISTS `ferremas` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `ferremas`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(5, 'administrador'),
(2, 'bodeguero'),
(1, 'cliente'),
(4, 'contador'),
(3, 'vendedor');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `auth_group_permissions`
--

INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 4),
(5, 1, 5),
(6, 1, 6),
(7, 1, 7),
(8, 1, 8),
(9, 1, 9),
(10, 1, 10),
(11, 1, 11),
(12, 1, 12),
(13, 1, 13),
(14, 1, 14),
(15, 1, 15),
(16, 1, 16),
(17, 1, 17),
(18, 1, 18),
(19, 1, 19),
(20, 1, 20),
(21, 1, 21),
(22, 1, 22),
(23, 1, 23),
(24, 1, 24),
(25, 2, 1),
(26, 2, 2),
(27, 2, 3),
(28, 2, 4),
(29, 2, 5),
(30, 2, 6),
(31, 2, 7),
(32, 2, 8),
(33, 2, 9),
(34, 2, 10),
(35, 2, 11),
(36, 2, 12),
(37, 2, 13),
(38, 2, 14),
(39, 2, 15),
(40, 2, 16),
(41, 2, 17),
(42, 2, 18),
(43, 2, 19),
(44, 2, 20),
(45, 2, 21),
(46, 2, 22),
(47, 2, 23),
(48, 2, 24),
(49, 3, 1),
(50, 3, 2),
(51, 3, 3),
(52, 3, 4),
(53, 3, 5),
(54, 3, 6),
(55, 3, 7),
(56, 3, 8),
(57, 3, 9),
(58, 3, 10),
(59, 3, 11),
(60, 3, 12),
(61, 3, 13),
(62, 3, 14),
(63, 3, 15),
(64, 3, 16),
(65, 3, 17),
(66, 3, 18),
(67, 3, 19),
(68, 3, 20),
(69, 3, 21),
(70, 3, 22),
(71, 3, 23),
(72, 3, 24),
(73, 4, 1),
(74, 4, 2),
(75, 4, 3),
(76, 4, 4),
(77, 4, 5),
(78, 4, 6),
(79, 4, 7),
(80, 4, 8),
(81, 4, 9),
(82, 4, 10),
(83, 4, 11),
(84, 4, 12),
(85, 4, 13),
(86, 4, 14),
(87, 4, 15),
(88, 4, 16),
(89, 4, 17),
(90, 4, 18),
(91, 4, 19),
(92, 4, 20),
(93, 4, 21),
(94, 4, 22),
(95, 4, 23),
(96, 4, 24),
(97, 5, 1),
(98, 5, 2),
(99, 5, 3),
(100, 5, 4),
(101, 5, 5),
(102, 5, 6),
(103, 5, 7),
(104, 5, 8),
(105, 5, 9),
(106, 5, 10),
(107, 5, 11),
(108, 5, 12),
(109, 5, 13),
(110, 5, 14),
(111, 5, 15),
(112, 5, 16),
(113, 5, 17),
(114, 5, 18),
(115, 5, 19),
(116, 5, 20),
(117, 5, 21),
(118, 5, 22),
(119, 5, 23),
(120, 5, 24);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add compras', 7, 'add_compras'),
(26, 'Can change compras', 7, 'change_compras'),
(27, 'Can delete compras', 7, 'delete_compras'),
(28, 'Can view compras', 7, 'view_compras'),
(29, 'Can add carrito', 8, 'add_carrito'),
(30, 'Can change carrito', 8, 'change_carrito'),
(31, 'Can delete carrito', 8, 'delete_carrito'),
(32, 'Can view carrito', 8, 'view_carrito'),
(33, 'Can add sucursal', 9, 'add_sucursal'),
(34, 'Can change sucursal', 9, 'change_sucursal'),
(35, 'Can delete sucursal', 9, 'delete_sucursal'),
(36, 'Can view sucursal', 9, 'view_sucursal'),
(37, 'Can add compra', 10, 'add_compra'),
(38, 'Can change compra', 10, 'change_compra'),
(39, 'Can delete compra', 10, 'delete_compra'),
(40, 'Can view compra', 10, 'view_compra'),
(41, 'Can add boleta', 11, 'add_boleta'),
(42, 'Can change boleta', 11, 'change_boleta'),
(43, 'Can delete boleta', 11, 'delete_boleta'),
(44, 'Can view boleta', 11, 'view_boleta'),
(45, 'Can add mensaje contacto', 12, 'add_mensajecontacto'),
(46, 'Can change mensaje contacto', 12, 'change_mensajecontacto'),
(47, 'Can delete mensaje contacto', 12, 'delete_mensajecontacto'),
(48, 'Can view mensaje contacto', 12, 'view_mensajecontacto'),
(49, 'Can add pedido aceptado', 13, 'add_pedidoaceptado'),
(50, 'Can change pedido aceptado', 13, 'change_pedidoaceptado'),
(51, 'Can delete pedido aceptado', 13, 'delete_pedidoaceptado'),
(52, 'Can view pedido aceptado', 13, 'view_pedidoaceptado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$216000$cLI6y2EcehAT$gfbnyWVa1p4MjPrwxaJiqLAWQ2/VbbUsWjHvoGkYnvk=', '2024-07-14 23:52:27.232822', 1, 'admin', 'ignacio', 'riffo', 'ig.riffo@duocuc.cl', 1, 1, '2024-05-07 20:30:16.000000'),
(2, 'pbkdf2_sha256$216000$31qf8qRXrSfC$rJ4ywWiRWUeYi01YKtH0WgtbGyQNSzl512MnFXPtaqw=', '2024-07-14 16:34:52.688508', 0, 'nacho', 'Ignacio', 'Riffo', 'ignacio.drp@gmail.com', 0, 1, '2024-05-07 23:50:38.353010'),
(3, 'pbkdf2_sha256$216000$8u5eBqitcfEm$Iw+MnPcow5VWFLMKtCe7FcG/3LKIrNLy2WHr5iyvvtU=', NULL, 0, 'david', '', '', 'david@gmail.com', 0, 1, '2024-05-08 18:26:54.000000'),
(4, 'pbkdf2_sha256$216000$yHf8vfe91XWI$ydxZPUb/qfk+qjyNMOUEXgf3p4lc3S6d5eajiGkaV+w=', '2024-05-24 17:11:36.935677', 0, 'paola', 'paola', 'uruutia', 'paola@gmail.com', 0, 1, '2024-05-24 17:11:36.734769'),
(5, 'pbkdf2_sha256$216000$1vSgD1Ep321R$fveVnzOMwHne6s58Htx971KPiilOijTFA//V1YC7lSw=', '2024-05-24 19:12:53.611473', 0, 'fabian', 'fabian andres', 'bravo rivas', 'fabian@gmail.com', 0, 1, '2024-05-24 19:12:53.417485'),
(6, 'pbkdf2_sha256$216000$8SNJlFTNXKBH$LBHv3kll92DRgLCKRyBWClXSF+yAAKxG+V1/9TWidHw=', '2024-05-27 01:15:56.130688', 0, 'daniel', 'daniel', 'galvez', 'daniel@gmail.com', 0, 1, '2024-05-24 19:19:27.675685'),
(7, 'pbkdf2_sha256$216000$Rp2yfEfLfwny$eBK8afDWG4+2VXpB8A1PhepxPuPDLBvP1Q2m9pB6qsY=', '2024-05-24 19:20:17.673285', 0, 'joaquin', 'joaquin', 'lopez', 'joaquin@gmail.com', 0, 1, '2024-05-24 19:20:17.470271'),
(8, 'pbkdf2_sha256$216000$SaCWQ8IA0j0q$ffYtj4dFSVjgT2IlrBotPPMTkfYVhkXYtCheUBWOmJA=', '2024-07-14 16:59:52.643596', 0, 'bodeguero', 'francisco', 'vera', 'fvera@gmail.com', 0, 1, '2024-05-26 22:53:03.417948'),
(9, 'pbkdf2_sha256$216000$iBXyYeCFcBFl$Zl/o5ezzLGPTvKnr9i9TvBIXmxLWhr5ykcjaH3iqp74=', '2024-07-14 16:43:01.198769', 0, 'contador', 'david', 'espinosa', 'da@gmail.com', 0, 1, '2024-05-27 00:30:43.504543');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(11, 1, 5),
(1, 2, 1),
(2, 3, 5),
(3, 4, 1),
(4, 5, 3),
(5, 6, 3),
(6, 7, 3),
(12, 8, 2),
(13, 9, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_boleta`
--

DROP TABLE IF EXISTS `core_boleta`;
CREATE TABLE `core_boleta` (
  `id` int(11) NOT NULL,
  `codigo` varchar(20) NOT NULL,
  `total` int(11) NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `transferencia` tinyint(1) NOT NULL,
  `validacion` tinyint(1) DEFAULT NULL,
  `aceptado` tinyint(1) NOT NULL,
  `bodeguero_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `core_boleta`
--

INSERT INTO `core_boleta` (`id`, `codigo`, `total`, `imagen`, `transferencia`, `validacion`, `aceptado`, `bodeguero_id`) VALUES
(6, '35312', 12345, 'IMG_2554_L7pMJD4.PNG', 1, 1, 0, NULL),
(8, 'b4e2d', 3870, 'IMG_2554.PNG', 1, 1, 1, 8),
(9, 'e2a3a', 5170, '', 0, 1, 1, 8),
(10, '4b0c9', 5990, 'IMG_2554_oJhDHq0.PNG', 1, 0, 0, NULL),
(11, '59ea4', 1980, '', 1, 0, 0, NULL),
(12, '85973', 1990, '', 0, 1, 1, 8),
(13, 'cbb4f', 10930, 'CP36.png', 1, 0, 0, NULL),
(14, 'eab57', 14990, '', 0, 1, 0, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_carrito`
--

DROP TABLE IF EXISTS `core_carrito`;
CREATE TABLE `core_carrito` (
  `id` int(11) NOT NULL,
  `producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `vigente` tinyint(1) NOT NULL,
  `cliente_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `core_carrito`
--

INSERT INTO `core_carrito` (`id`, `producto`, `cantidad`, `vigente`, `cliente_id`) VALUES
(31, 11, 1, 0, 2),
(32, 12, 1, 0, 2),
(33, 2, 1, 0, 2),
(34, 10, 3, 0, 2),
(36, 12, 2, 0, 2),
(37, 1, 1, 0, 2),
(38, 7, 1, 0, 2),
(39, 2, 2, 0, 2),
(40, 1, 1, 0, 2),
(48, 1, 4, 0, 2),
(49, 2, 3, 0, 2),
(50, 4, 1, 0, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_compra`
--

DROP TABLE IF EXISTS `core_compra`;
CREATE TABLE `core_compra` (
  `id` int(11) NOT NULL,
  `codigo` varchar(20) NOT NULL,
  `retiro` tinyint(1) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `fecha` date NOT NULL,
  `carrito_id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `sucursal_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `core_compra`
--

INSERT INTO `core_compra` (`id`, `codigo`, `retiro`, `direccion`, `fecha`, `carrito_id`, `cliente_id`, `sucursal_id`) VALUES
(14, '35312', 1, '', '2024-05-23', 31, 2, 1),
(15, '35312', 1, '', '2024-05-23', 32, 2, 1),
(17, 'b4e2d', 1, '', '2024-05-23', 34, 2, 1),
(18, 'e2a3a', 0, 'av las nieves 02196', '2024-05-23', 36, 2, NULL),
(19, 'e2a3a', 0, 'av las nieves 02196', '2024-05-23', 37, 2, NULL),
(20, '4b0c9', 1, '', '2024-05-23', 38, 2, 4),
(21, '59ea4', 0, 'av las nieves 02196', '2024-05-23', 39, 2, NULL),
(22, '85973', 1, '', '2024-05-23', 40, 2, 3),
(23, 'cbb4f', 0, 'Av las nieves 02196', '2024-06-19', 48, 2, NULL),
(24, 'cbb4f', 0, 'Av las nieves 02196', '2024-06-19', 49, 2, NULL),
(25, 'eab57', 1, '', '2024-06-19', 50, 2, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_mensajecontacto`
--

DROP TABLE IF EXISTS `core_mensajecontacto`;
CREATE TABLE `core_mensajecontacto` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(254) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `asunto` varchar(200) NOT NULL,
  `mensaje` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `core_mensajecontacto`
--

INSERT INTO `core_mensajecontacto` (`id`, `nombre`, `correo`, `telefono`, `asunto`, `mensaje`) VALUES
(1, 'ignacio', 'ignacio.drp@gmail.com', '968372903', 'Presupuesto martillo', 'hgola mundo'),
(2, 'ignacio', 'ignacio.drp@gmail.com', '968372903', 'Presupuesto martillo', 'hola mundo'),
(3, 'ignacio', 'ignacio.drp@gmail.com', '968372903', 'Presupuesto martillo', 'jhbkhbkbjbkjbjbjkbjkbjk'),
(4, 'ignacio', 'ignacio.drp@gmail.com', '968372903', 'Presupuesto martillo', 'jfsajkjsadksdak'),
(5, 'ignacio david riffo peña', 'ignacio.drp@gmail.com', '968372903', 'Presupuesto martillo', 'Caso de prueba 41'),
(6, 'ignacio david riffo peña', 'ignacio.drp@gmail.com', '968372903', 'Presupuesto martillo', 'Caso de prueba 41'),
(7, 'ignacio david riffo peña', 'ignacio.drp@gmail.com', '968372903', 'Presupuesto martillo', 'Caso de prueba 41');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_sucursal`
--

DROP TABLE IF EXISTS `core_sucursal`;
CREATE TABLE `core_sucursal` (
  `id` int(11) NOT NULL,
  `nombre` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `core_sucursal`
--

INSERT INTO `core_sucursal` (`id`, `nombre`) VALUES
(1, 'Las Condes'),
(2, 'La Florida'),
(3, 'Puente Alto'),
(4, 'Maipú');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2024-05-07 23:42:04.252706', '1', 'cliente', 1, '[{\"added\": {}}]', 3, 1),
(2, '2024-05-07 23:42:08.903689', '1', 'cliente', 2, '[]', 3, 1),
(3, '2024-05-08 18:25:59.589493', '2', 'bodeguero', 1, '[{\"added\": {}}]', 3, 1),
(4, '2024-05-08 18:26:08.455992', '3', 'vendedor', 1, '[{\"added\": {}}]', 3, 1),
(5, '2024-05-08 18:26:17.689682', '4', 'contador', 1, '[{\"added\": {}}]', 3, 1),
(6, '2024-05-08 18:26:28.572752', '5', 'administrador', 1, '[{\"added\": {}}]', 3, 1),
(7, '2024-05-08 18:26:54.373310', '3', 'david', 1, '[{\"added\": {}}]', 4, 1),
(8, '2024-05-08 18:27:06.805868', '3', 'david', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(9, '2024-05-08 18:27:21.705931', '3', 'david', 2, '[{\"changed\": {\"fields\": [\"Email address\"]}}]', 4, 1),
(10, '2024-05-08 18:27:35.840018', '3', 'david', 2, '[{\"changed\": {\"fields\": [\"Email address\"]}}]', 4, 1),
(11, '2024-05-25 01:53:50.080211', '1', 'admin', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Groups\"]}}]', 4, 1),
(12, '2024-05-25 01:54:11.814905', '1', 'admin', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(11, 'core', 'boleta'),
(8, 'core', 'carrito'),
(10, 'core', 'compra'),
(7, 'core', 'compras'),
(12, 'core', 'mensajecontacto'),
(13, 'core', 'pedidoaceptado'),
(9, 'core', 'sucursal'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-05-07 20:26:49.051272'),
(2, 'auth', '0001_initial', '2024-05-07 20:26:49.441582'),
(3, 'admin', '0001_initial', '2024-05-07 20:26:50.139333'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-05-07 20:26:50.359163'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-05-07 20:26:50.373575'),
(6, 'contenttypes', '0002_remove_content_type_name', '2024-05-07 20:26:50.454806'),
(7, 'auth', '0002_alter_permission_name_max_length', '2024-05-07 20:26:50.553880'),
(8, 'auth', '0003_alter_user_email_max_length', '2024-05-07 20:26:50.575094'),
(9, 'auth', '0004_alter_user_username_opts', '2024-05-07 20:26:50.587596'),
(10, 'auth', '0005_alter_user_last_login_null', '2024-05-07 20:26:50.655450'),
(11, 'auth', '0006_require_contenttypes_0002', '2024-05-07 20:26:50.655450'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2024-05-07 20:26:50.680999'),
(13, 'auth', '0008_alter_user_username_max_length', '2024-05-07 20:26:50.706202'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2024-05-07 20:26:50.726758'),
(15, 'auth', '0010_alter_group_name_max_length', '2024-05-07 20:26:50.754161'),
(16, 'auth', '0011_update_proxy_permissions', '2024-05-07 20:26:50.762497'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2024-05-07 20:26:50.789542'),
(18, 'sessions', '0001_initial', '2024-05-07 20:26:50.829057'),
(19, 'core', '0001_initial', '2024-05-21 03:12:19.780722'),
(20, 'core', '0002_auto_20240522_1450', '2024-05-22 18:51:02.548952'),
(21, 'core', '0003_auto_20240522_1451', '2024-05-22 18:51:42.539977'),
(22, 'core', '0004_auto_20240522_1605', '2024-05-22 20:05:28.650930'),
(23, 'core', '0005_boleta', '2024-05-22 21:12:54.308078'),
(24, 'core', '0006_remove_compra_contacto', '2024-05-22 21:50:28.987312'),
(25, 'core', '0007_auto_20240522_2354', '2024-05-23 03:55:01.519149'),
(26, 'core', '0008_auto_20240524_1312', '2024-05-24 17:12:46.326225'),
(27, 'core', '0009_auto_20240526_1858', '2024-05-26 22:59:17.345797'),
(28, 'core', '0010_delete_pedidoaceptado', '2024-05-27 00:21:56.600458');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1124t96bnjn6ifpkk6xsegh6ducw4619', '.eJxVjEEOwiAQRe_C2pBSCgMu3XsGwgyMVA0kpV0Z765NutDtf-_9lwhxW0vYel7CnMRZjOL0u2GkR647SPdYb01Sq-syo9wVedAury3l5-Vw_w5K7OVbA3oiqy1PNNHogI3TlIwyDCoxaK_ZM-sIDj068moAa73KFtkBDizeH-otOAc:1sLtud:YAiTRxRvppD320X5U_rbVb5srA4SLAIPD3obzT2oWLU', '2024-07-09 00:19:55.067825'),
('hmbw4yh80wrc9dnhi9pbs3g0qo7dmg2m', '.eJxVjEsOwjAMBe-SNYpM66Q1S_Y9Q-S4NimgVupnhbg7VOoCtm9m3ssl3taStkXnNPTu4lp3-t0yy0PHHfR3Hm-Tl2lc5yH7XfEHXXw39fq8Hu7fQeGlfGsiQqNKgpIxKMQKLaO0TZOlqWuIAmpKEDUgnc2w4owEFOo2BGZ07w_ipDeU:1sBOz3:yPN-PRsztEE74WT8v3yHUaM7F-5D0xzuknHxQUq9GV0', '2024-06-10 01:17:05.540073'),
('qx4uw2dskpmjqu1tw14vqvhpo3fgkpv3', 'e30:1s4l4h:aGhLIYcNQK5Yc8sM41e2judc0DxIu5ysY1A8tNkv_xQ', '2024-05-22 17:27:27.336051');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `core_boleta`
--
ALTER TABLE `core_boleta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_boleta_bodeguero_id_1b7cbb13_fk_auth_user_id` (`bodeguero_id`);

--
-- Indices de la tabla `core_carrito`
--
ALTER TABLE `core_carrito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_carrito_cliente_id_8efb49fb_fk_auth_user_id` (`cliente_id`);

--
-- Indices de la tabla `core_compra`
--
ALTER TABLE `core_compra`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_compra_carrito_id_852b20e6_fk_core_carrito_id` (`carrito_id`),
  ADD KEY `core_compra_cliente_id_dab1b96e_fk_auth_user_id` (`cliente_id`),
  ADD KEY `core_compra_sucursal_id_20927f57_fk_core_sucursal_id` (`sucursal_id`);

--
-- Indices de la tabla `core_mensajecontacto`
--
ALTER TABLE `core_mensajecontacto`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `core_sucursal`
--
ALTER TABLE `core_sucursal`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `core_boleta`
--
ALTER TABLE `core_boleta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `core_carrito`
--
ALTER TABLE `core_carrito`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `core_compra`
--
ALTER TABLE `core_compra`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `core_mensajecontacto`
--
ALTER TABLE `core_mensajecontacto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `core_sucursal`
--
ALTER TABLE `core_sucursal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `core_boleta`
--
ALTER TABLE `core_boleta`
  ADD CONSTRAINT `core_boleta_bodeguero_id_1b7cbb13_fk_auth_user_id` FOREIGN KEY (`bodeguero_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `core_carrito`
--
ALTER TABLE `core_carrito`
  ADD CONSTRAINT `core_carrito_cliente_id_8efb49fb_fk_auth_user_id` FOREIGN KEY (`cliente_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `core_compra`
--
ALTER TABLE `core_compra`
  ADD CONSTRAINT `core_compra_carrito_id_852b20e6_fk_core_carrito_id` FOREIGN KEY (`carrito_id`) REFERENCES `core_carrito` (`id`),
  ADD CONSTRAINT `core_compra_cliente_id_dab1b96e_fk_auth_user_id` FOREIGN KEY (`cliente_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `core_compra_sucursal_id_20927f57_fk_core_sucursal_id` FOREIGN KEY (`sucursal_id`) REFERENCES `core_sucursal` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

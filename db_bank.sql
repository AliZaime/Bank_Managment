-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : dim. 09 fév. 2025 à 16:39
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `db_bank`
--

-- --------------------------------------------------------

--
-- Structure de la table `checking_accounts`
--

CREATE TABLE `checking_accounts` (
  `id` int(11) NOT NULL,
  `balance` decimal(15,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `transaction_count` int(11) NOT NULL DEFAULT 0,
  `userID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `checking_accounts`
--

INSERT INTO `checking_accounts` (`id`, `balance`, `created_at`, `transaction_count`, `userID`) VALUES
(1, 4049.60, '2024-12-27 20:01:41', 5, NULL),
(2, 2600.00, '2024-12-27 20:01:41', 1, NULL),
(3, 600.00, '2024-12-27 20:01:41', 2, NULL),
(7, 3000.00, '2025-02-05 21:48:27', 0, NULL),
(8, 3000.00, '2025-02-05 21:55:11', 0, 2);

-- --------------------------------------------------------

--
-- Structure de la table `saving_accounts`
--

CREATE TABLE `saving_accounts` (
  `id` int(11) NOT NULL,
  `balance` decimal(15,2) NOT NULL,
  `interest_rate` decimal(5,4) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `userid` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `saving_accounts`
--

INSERT INTO `saving_accounts` (`id`, `balance`, `interest_rate`, `created_at`, `userid`) VALUES
(8, 6500.00, 0.0100, '2024-12-28 17:34:28', NULL),
(9, 7500.00, 0.0300, '2024-12-28 17:34:37', NULL),
(10, 6840.00, 0.0100, '2024-12-30 16:30:18', NULL),
(11, 6800.00, 0.0200, '2025-02-04 19:40:30', NULL),
(12, 1000.00, 0.0500, '2025-02-05 21:33:24', 2),
(13, 2500.00, 0.0200, '2025-02-05 21:47:27', 3);

-- --------------------------------------------------------

--
-- Structure de la table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  `account_type` enum('Saving','Checking') NOT NULL,
  `transaction_type` enum('Deposit','Withdraw','Transfer In','Transfer Out','Fee','Interest') NOT NULL,
  `amount` decimal(15,2) NOT NULL,
  `transaction_date` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `transactions`
--

INSERT INTO `transactions` (`id`, `account_id`, `account_type`, `transaction_type`, `amount`, `transaction_date`) VALUES
(1, 8, 'Saving', 'Transfer Out', 1000.00, '2025-02-05 19:19:17'),
(2, 9, 'Saving', 'Transfer In', 1000.00, '2025-02-05 19:19:17'),
(3, 1, 'Checking', 'Withdraw', 500.00, '2025-02-08 17:04:38'),
(4, 1, 'Checking', 'Fee', 0.20, '2025-02-08 17:04:38'),
(5, 1, 'Checking', 'Withdraw', 400.00, '2025-02-08 17:09:32'),
(6, 1, 'Checking', 'Fee', 0.20, '2025-02-08 17:09:32'),
(7, 1, 'Checking', 'Withdraw', 99.00, '2025-02-08 17:11:35'),
(8, 1, 'Checking', 'Fee', 0.20, '2025-02-08 17:11:35'),
(9, 1, 'Checking', 'Deposit', 100.00, '2025-02-08 23:04:09'),
(10, 1, 'Checking', 'Fee', 0.40, '2025-02-08 23:04:09'),
(11, 1, 'Checking', 'Withdraw', 50.00, '2025-02-08 23:04:29'),
(12, 1, 'Checking', 'Fee', 0.40, '2025-02-08 23:04:29'),
(13, 8, 'Saving', 'Transfer Out', 500.00, '2025-02-08 23:16:19'),
(14, 9, 'Saving', 'Transfer In', 500.00, '2025-02-08 23:16:19');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `isadmin` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `created_at`, `isadmin`) VALUES
(1, 'admin', 'admin@esisa.ma', '$2b$12$EjeVXzqbbEae0adziTMTGuPMtUh3tI2ol.IQ/OUEJnDsetZgdFxLK', '2025-02-05 20:23:33', 1),
(2, 'hamza rais', 'hmizourais557@gmail.com', '$2b$12$RRiK1WPDd0sBRftKCpo2/uF/j2bDBVZXva9ub4QF1GIKaX6GaCAmK', '2025-02-05 20:29:31', 0),
(3, 'ali zaime', 'alizaime2003@gmail.com', '$2b$12$69g8JWFfvLgh1oSYcElXv.zy.LgSvaMO2yyFYw7Ky17KeZ8wWDxj.', '2025-02-05 20:41:18', 0);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `checking_accounts`
--
ALTER TABLE `checking_accounts`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `saving_accounts`
--
ALTER TABLE `saving_accounts`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `checking_accounts`
--
ALTER TABLE `checking_accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `saving_accounts`
--
ALTER TABLE `saving_accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT pour la table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

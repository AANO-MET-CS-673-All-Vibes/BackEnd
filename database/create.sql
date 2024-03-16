CREATE TABLE IF NOT EXISTS `accounts` (
	`id` varchar(36) NOT NULL UNIQUE,
	`email` varchar(50) NOT NULL UNIQUE,
	`created` timestamp,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `users` (
	`id` varchar(36) NOT NULL UNIQUE,
	`internal_id` varchar(36) NOT NULL UNIQUE,
	`name` varchar(50),
	`gender` int,
	`dob` date,
	`bio` varchar(300),
	`image` varchar(255),
	`top_tracks` json,
	`top_artists` json,
	`last_updated` date,
	`last_online` timestamp,
	`like_count` int,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `matches` (
	`id1` varchar(36) NOT NULL,
	`id2` varchar(36) NOT NULL,
	`matched` tinyint(1),
	`unmatched` tinyint(1),
	`attempt_time` timestamp,
	`match_time` timestamp,
	`unmatch_time` timestamp
);

CREATE TABLE IF NOT EXISTS `messages` (
	`from` varchar(36) NOT NULL,
	`to` varchar(36) NOT NULL,
	`read` tinyint(1),
	`sent_time` timestamp,
	`read_time` timestamp,
	`text` varchar(500),
	`attachment` varchar(500)
);


ALTER TABLE `users` ADD CONSTRAINT `users_fk0` FOREIGN KEY (`id`) REFERENCES `accounts`(`id`);
ALTER TABLE `matches` ADD CONSTRAINT `matches_fk0` FOREIGN KEY (`id1`) REFERENCES `users`(`internal_id`);

ALTER TABLE `matches` ADD CONSTRAINT `matches_fk1` FOREIGN KEY (`id2`) REFERENCES `users`(`internal_id`);
ALTER TABLE `messages` ADD CONSTRAINT `messages_fk0` FOREIGN KEY (`from`) REFERENCES `users`(`internal_id`);

ALTER TABLE `messages` ADD CONSTRAINT `messages_fk1` FOREIGN KEY (`to`) REFERENCES `users`(`internal_id`);
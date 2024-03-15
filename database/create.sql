CREATE TABLE IF NOT EXISTS `account` (
	`id` varchar(36) NOT NULL UNIQUE,
	`email` varchar(50) NOT NULL UNIQUE,
	`created` timestamp,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `user` (
	`id` varchar(36) NOT NULL UNIQUE,
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

CREATE TABLE IF NOT EXISTS `match` (
	`id1` varchar(36) NOT NULL,
	`id2` varchar(36) NOT NULL,
	`matched` tinyint(1),
	`unmatched` tinyint(1),
	`attempt_time` timestamp,
	`match_time` timestamp,
	`unmatch_time` timestamp
);

CREATE TABLE IF NOT EXISTS `message` (
	`from` varchar(36) NOT NULL,
	`to` varchar(36) NOT NULL,
	`read` tinyint(1),
	`sent_time` timestamp,
	`read_time` timestamp,
	`text` varchar(500),
	`attachment` varchar(500)
);


ALTER TABLE `user` ADD CONSTRAINT `user_fk0` FOREIGN KEY (`id`) REFERENCES `account`(`id`);
ALTER TABLE `match` ADD CONSTRAINT `match_fk0` FOREIGN KEY (`id1`) REFERENCES `user`(`id`);

ALTER TABLE `match` ADD CONSTRAINT `match_fk1` FOREIGN KEY (`id2`) REFERENCES `user`(`id`);
ALTER TABLE `message` ADD CONSTRAINT `message_fk0` FOREIGN KEY (`from`) REFERENCES `user`(`id`);

ALTER TABLE `message` ADD CONSTRAINT `message_fk1` FOREIGN KEY (`to`) REFERENCES `user`(`id`);
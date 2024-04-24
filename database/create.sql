CREATE TABLE IF NOT EXISTS `accounts` (
	`id` varchar(36) NOT NULL UNIQUE,
	`encrypted_email` varchar(50) NOT NULL UNIQUE,
	`created` timestamp,
	PRIMARY KEY (`encrypted_id`)
);

CREATE TABLE IF NOT EXISTS `users` (
	`id` varchar(36) NOT NULL UNIQUE,
	`internal_id` varchar(36) NOT NULL UNIQUE,
	`encrypted_name` varchar(50),
	`encrypted_gender` int,
	`encrypted_dob` date,
	`encrypted_bio` varchar(300),
	`image` varchar(255),
	'top_tracks` json,
	`top_artists` json,
	`last_updated` date,
	`last_online` timestamp,
	`like_count` int,
	PRIMARY KEY (`encrypted_id`)
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
	`sender` varchar(36) NOT NULL,
	`recipient` varchar(36) NOT NULL,
	`seen` tinyint(1),
	`sent_time` timestamp,
	`seen_time` timestamp,
	`encrypted_text` varchar(500),
	`encrypted_attachment` varchar(500)
);


ALTER TABLE `users` ADD CONSTRAINT `users_fk0` FOREIGN KEY (`encrypted_id`) REFERENCES `accounts`(`encrypted_id`);
ALTER TABLE `matches` ADD CONSTRAINT `matches_fk0` FOREIGN KEY (`encrypted_id1`) REFERENCES `users`(`encrypted_internal_id`);

ALTER TABLE `matches` ADD CONSTRAINT `matches_fk1` FOREIGN KEY (`encrypted_id2`) REFERENCES `users`(`encrypted_internal_id`);
ALTER TABLE `messages` ADD CONSTRAINT `messages_fk0` FOREIGN KEY (`from`) REFERENCES `users`(`encrypted_internal_id`);

ALTER TABLE `messages` ADD CONSTRAINT `messages_fk1` FOREIGN KEY (`to`) REFERENCES `users`(`encrypted_internal_id`);

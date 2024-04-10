CREATE TABLE IF NOT EXISTS `accounts` (
	`encrypted_id` varchar(36) NOT NULL UNIQUE,
	`encrypted_email` varchar(50) NOT NULL UNIQUE,
	`created` timestamp,
	PRIMARY KEY (`encrypted_id`)
);

CREATE TABLE IF NOT EXISTS `users` (
	`encrypted_id` varchar(36) NOT NULL UNIQUE,
	`encrypted_internal_id` varchar(36) NOT NULL UNIQUE,
	`encrypted_name` varchar(50),
	`encrypted_gender` int,
	`encrypted_dob` date,
	`encrypted_bio` varchar(300),
	`encrypted_image` varchar(255),
	`encrypted_top_tracks` json,
	`encrypted_top_artists` json,
	`encrypted_last_updated` date,
	`encrypted_last_online` timestamp,
	`encrypted_like_count` int,
	PRIMARY KEY (`encrypted_id`)
);

CREATE TABLE IF NOT EXISTS `matches` (
	`encrypted_id1` varchar(36) NOT NULL,
	`encrypted_id2` varchar(36) NOT NULL,
	`encrypted_matched` tinyint(1),
	`encrypted_unmatched` tinyint(1),
	`encrypted_attempt_time` timestamp,
	`encrypted_match_time` timestamp,
	`encrypted_unmatch_time` timestamp
);

CREATE TABLE IF NOT EXISTS `messages` (
	`encrypted_sender` varchar(36) NOT NULL,
	`encrypted_recipient` varchar(36) NOT NULL,
	`encrypted_seen` tinyint(1),
	`encrypted_sent_time` timestamp,
	`encrypted_seen_time` timestamp,
	`encrypted_text` varchar(500),
	`encrypted_attachment` varchar(500)
);


ALTER TABLE `users` ADD CONSTRAINT `users_fk0` FOREIGN KEY (`encrypted_id`) REFERENCES `accounts`(`encrypted_id`);
ALTER TABLE `matches` ADD CONSTRAINT `matches_fk0` FOREIGN KEY (`encrypted_id1`) REFERENCES `users`(`encrypted_internal_id`);

ALTER TABLE `matches` ADD CONSTRAINT `matches_fk1` FOREIGN KEY (`encrypted_id2`) REFERENCES `users`(`encrypted_internal_id`);
ALTER TABLE `messages` ADD CONSTRAINT `messages_fk0` FOREIGN KEY (`from`) REFERENCES `users`(`encrypted_internal_id`);

ALTER TABLE `messages` ADD CONSTRAINT `messages_fk1` FOREIGN KEY (`to`) REFERENCES `users`(`encrypted_internal_id`);

-- 1. 데이터베이스 생성 (이미 있으면 생략)
CREATE DATABASE IF NOT EXISTS news_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 2. 해당 데이터베이스 사용
USE news_db;

-- 3. 테이블 생성 (존재하지 않을 경우만)
CREATE TABLE IF NOT EXISTS word_list (
    id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    append_word VARCHAR(255) NOT NULL,
    append_date VARCHAR(10) NOT NULL,
    append_count INT DEFAULT 0
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
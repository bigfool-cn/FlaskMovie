/*
 Navicat Premium Data Transfer

 Source Server         : 腾讯云
 Source Server Type    : MySQL
 Source Server Version : 50721
 Source Host           : 193.112.43.41:3306
 Source Schema         : movie

 Target Server Type    : MySQL
 Target Server Version : 50721
 File Encoding         : 65001

 Date: 31/03/2019 15:35:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pwd` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `is_super` smallint(6) NULL DEFAULT NULL,
  `role_id` int(11) NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `role_id`(`role_id`) USING BTREE,
  INDEX `ix_admin_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES (1, 'admin', 'pbkdf2:sha256:50000$TIPc6irS$a7ae9ff1cf7842473a387db3d1f41377a3a093a775c5b55912fbd3c6fb31013b', 0, 1, '2018-01-18 22:04:22');
INSERT INTO `admin` VALUES (2, 'Devil', 'pbkdf2:sha256:50000$nAVOBIEt$78f08701479a7fd7e523ee5125867f3e9e464e032ccc5378a9db471fc639093d', 1, 2, '2018-01-24 20:28:18');

-- ----------------------------
-- Table structure for adminlog
-- ----------------------------
DROP TABLE IF EXISTS `adminlog`;
CREATE TABLE `adminlog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) NULL DEFAULT NULL,
  `ip` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `admin_id`(`admin_id`) USING BTREE,
  INDEX `ix_adminlog_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of adminlog
-- ----------------------------
INSERT INTO `adminlog` VALUES (1, 1, '127.0.0.1', '2018-01-22 21:02:45');
INSERT INTO `adminlog` VALUES (2, 1, '127.0.0.1', '2018-01-22 21:03:03');
INSERT INTO `adminlog` VALUES (3, 1, '127.0.0.1', '2018-01-23 19:42:50');
INSERT INTO `adminlog` VALUES (4, 2, '127.0.0.1', '2018-01-24 21:00:11');
INSERT INTO `adminlog` VALUES (5, 1, '127.0.0.1', '2018-01-24 21:04:00');
INSERT INTO `adminlog` VALUES (6, 1, '127.0.0.1', '2018-01-24 21:12:42');
INSERT INTO `adminlog` VALUES (7, 2, '127.0.0.1', '2018-01-24 21:14:50');
INSERT INTO `adminlog` VALUES (8, 1, '127.0.0.1', '2018-01-24 21:20:19');
INSERT INTO `adminlog` VALUES (9, 2, '127.0.0.1', '2018-06-24 18:09:21');
INSERT INTO `adminlog` VALUES (10, 1, '127.0.0.1', '2018-06-25 10:04:00');

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('20f39fd842c6');

-- ----------------------------
-- Table structure for auth
-- ----------------------------
DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `ix_auth_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth
-- ----------------------------
INSERT INTO `auth` VALUES (1, '添加标签', '/admin/tag/add/', '2018-01-23 19:55:49');
INSERT INTO `auth` VALUES (2, '标签列表', '/admin/tag/list/<int:page>/', '2018-01-23 19:56:53');
INSERT INTO `auth` VALUES (3, '修改标签', '/admin/tag/edit/<int:id>/', '2018-01-23 19:57:27');
INSERT INTO `auth` VALUES (4, '删除标签', '/admin/tag/del/<int:id>/', '2018-01-23 19:58:11');

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `movie_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `movie_id`(`movie_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_comment_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of comment
-- ----------------------------
INSERT INTO `comment` VALUES (1, '好看', NULL, 1, '2018-01-21 20:42:09');
INSERT INTO `comment` VALUES (2, '还好', NULL, 1, '2018-01-21 20:42:37');
INSERT INTO `comment` VALUES (3, '<p><img src=\"http://img.baidu.com/hi/jx2/j_0002.gif\"/>好看</p>', NULL, 2, '2018-01-27 21:17:32');
INSERT INTO `comment` VALUES (4, '<p><img src=\"http://img.baidu.com/hi/jx2/j_0004.gif\"/>太好看了</p>', NULL, 2, '2018-01-27 21:18:52');
INSERT INTO `comment` VALUES (5, '<p><img src=\"http://img.baidu.com/hi/jx2/j_0015.gif\"/>可以的</p>', NULL, 2, '2018-01-27 21:52:54');

-- ----------------------------
-- Table structure for movie
-- ----------------------------
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `info` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `logo` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `star` smallint(6) NULL DEFAULT NULL,
  `playnum` bigint(20) NULL DEFAULT NULL,
  `commentnum` bigint(20) NULL DEFAULT NULL,
  `tag_id` int(11) NULL DEFAULT NULL,
  `area` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `release_time` date NULL DEFAULT NULL,
  `length` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `logo`(`logo`) USING BTREE,
  UNIQUE INDEX `title`(`title`) USING BTREE,
  UNIQUE INDEX `url`(`url`) USING BTREE,
  INDEX `tag_id`(`tag_id`) USING BTREE,
  INDEX `ix_movie_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `movie_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of movie
-- ----------------------------
INSERT INTO `movie` VALUES (3, '惊吓的小狗', '201806251111503254e20059b544e2bd261e2682a3ff08.mp4', '别吓的小狗', '2018062511170708e0e2d0aa2549e69ab358f94243f4df.png', 2, 0, 0, 7, '中国', '2018-06-30', '20', '2018-06-25 11:11:51');
INSERT INTO `movie` VALUES (4, '金毛与猫', '20180625111411294aef4f9c7d48a0b5502e987c0f472f.mp4', '金毛与猫', '2018062511141106fbd5b47211485b9210edd3e8ed293f.png', 1, 1, 0, 1, '中国', '2018-06-20', '20', '2018-06-25 11:14:12');
INSERT INTO `movie` VALUES (5, '二哈', '2018062511201169c480011a6e4bd3a8d3dcfb9cab40cd.mp4', '二哈', '20180625112011dece62e09942402c829f10664e0da9dd.png', 1, 1, 0, 2, '中国', '2018-06-21', '20', '2018-06-25 11:20:11');

-- ----------------------------
-- Table structure for moviecol
-- ----------------------------
DROP TABLE IF EXISTS `moviecol`;
CREATE TABLE `moviecol`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `movie_id`(`movie_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_moviecol_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `moviecol_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `moviecol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of moviecol
-- ----------------------------
INSERT INTO `moviecol` VALUES (1, NULL, 1, '2018-01-21 20:56:13');
INSERT INTO `moviecol` VALUES (2, NULL, 1, '2018-01-21 20:56:33');
INSERT INTO `moviecol` VALUES (3, NULL, 2, '2018-01-28 20:25:06');

-- ----------------------------
-- Table structure for oplog
-- ----------------------------
DROP TABLE IF EXISTS `oplog`;
CREATE TABLE `oplog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `ip` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `reason` varchar(600) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_oplog_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `oplog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `admin` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of oplog
-- ----------------------------
INSERT INTO `oplog` VALUES (1, 1, '127.0.0.1', '添加了一个标签：喜剧', '2018-01-22 20:46:30');
INSERT INTO `oplog` VALUES (2, 1, '127.0.0.1', '添加了一个标签：伦理', '2018-01-22 20:46:50');
INSERT INTO `oplog` VALUES (3, 1, '127.0.0.1', '添加了权限：admin→添加标签→/admin/tag/add/', '2018-01-23 19:55:50');
INSERT INTO `oplog` VALUES (4, 1, '127.0.0.1', '添加了权限：admin→标签列表→/admin/tag/list/<int:page>/', '2018-01-23 19:56:53');
INSERT INTO `oplog` VALUES (5, 1, '127.0.0.1', '添加了权限：admin→修改标签→/admin/tag/list/<int:id>/', '2018-01-23 19:57:27');
INSERT INTO `oplog` VALUES (6, 1, '127.0.0.1', '添加了权限：admin→删除标签→/admin/tag/del/<int:id>/', '2018-01-23 19:58:11');
INSERT INTO `oplog` VALUES (7, 1, '127.0.0.1', '修改了权限：admin→修改标签→/admin/tag/edit/<int:id>/：修改标签→/admin/tag/edit/<int:id>/', '2018-01-23 20:28:07');
INSERT INTO `oplog` VALUES (8, 1, '127.0.0.1', '添加了权限：admin→adad→adsds/sdf/sfs', '2018-01-23 20:30:05');
INSERT INTO `oplog` VALUES (9, 1, '127.0.0.1', '修改了权限：admin→adad15131→adsds/sdf/sfs：adad15131→adsds/sdf/sfs', '2018-01-23 20:30:17');
INSERT INTO `oplog` VALUES (10, 1, '127.0.0.1', '删除了一个权限：admin→adad15131', '2018-01-23 20:30:25');
INSERT INTO `oplog` VALUES (11, 1, '127.0.0.1', '添加了一个角色：admin→标签管理员', '2018-01-23 20:59:00');
INSERT INTO `oplog` VALUES (12, 1, '127.0.0.1', '添加了一个角色：admin→标签管理员1', '2018-01-23 21:05:02');
INSERT INTO `oplog` VALUES (13, 1, '127.0.0.1', '添加了一个角色：admin→标签管理员2', '2018-01-23 21:05:15');
INSERT INTO `oplog` VALUES (14, 1, '127.0.0.1', '删除了一个角色：admin→标签管理员2', '2018-01-23 21:07:47');
INSERT INTO `oplog` VALUES (15, 1, '127.0.0.1', '修改了角色：admin→标签管理员1：标签管理员1', '2018-01-23 21:30:31');
INSERT INTO `oplog` VALUES (16, 1, '127.0.0.1', '修改了角色：admin→标签管理员：标签管理员', '2018-01-23 21:30:45');
INSERT INTO `oplog` VALUES (17, 1, '127.0.0.1', '添加了一个管理员：admin→Devil', '2018-01-24 20:28:19');
INSERT INTO `oplog` VALUES (18, 2, '127.0.0.1', '添加了一个标签：情色', '2018-01-26 17:17:04');
INSERT INTO `oplog` VALUES (19, 2, '127.0.0.1', '删除了一部电影：汤不热-1', '2018-06-24 18:09:34');
INSERT INTO `oplog` VALUES (20, 2, '127.0.0.1', '删除了一部电影：汤不热', '2018-06-24 18:09:36');
INSERT INTO `oplog` VALUES (21, 2, '127.0.0.1', '添加了一个预告：大闹天空', '2018-06-24 18:12:59');
INSERT INTO `oplog` VALUES (22, 2, '127.0.0.1', '添加了一个预告：捉妖记', '2018-06-24 18:13:22');
INSERT INTO `oplog` VALUES (23, 2, '127.0.0.1', '添加了一个预告：唐人街探案2', '2018-06-24 18:13:47');
INSERT INTO `oplog` VALUES (24, 2, '127.0.0.1', '添加了一个预告：红海行动', '2018-06-24 18:14:28');
INSERT INTO `oplog` VALUES (25, 1, '127.0.0.1', '添加了一部电影：惊吓的小狗', '2018-06-25 11:11:51');
INSERT INTO `oplog` VALUES (26, 1, '127.0.0.1', '添加了一部电影：金毛与猫', '2018-06-25 11:14:12');
INSERT INTO `oplog` VALUES (27, 1, '127.0.0.1', '修改了电影信息：惊吓的小狗', '2018-06-25 11:17:07');
INSERT INTO `oplog` VALUES (28, 1, '127.0.0.1', '添加了一部电影：二哈', '2018-06-25 11:20:11');

-- ----------------------------
-- Table structure for preview
-- ----------------------------
DROP TABLE IF EXISTS `preview`;
CREATE TABLE `preview`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `logo` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `logo`(`logo`) USING BTREE,
  UNIQUE INDEX `title`(`title`) USING BTREE,
  INDEX `ix_preview_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of preview
-- ----------------------------
INSERT INTO `preview` VALUES (1, '龙珠', '20180121173348287d0d48747642df835c5e1033b9243c.jpg', '2018-01-21 16:50:47');
INSERT INTO `preview` VALUES (2, '大闹天空', '2018062418125936119a1b3f2d4de8af2a9dee465d0b2e.jpg', '2018-06-24 18:12:59');
INSERT INTO `preview` VALUES (3, '捉妖记', '201806241813210632633ee8bf48139527c757600a5689.jpg', '2018-06-24 18:13:22');
INSERT INTO `preview` VALUES (4, '唐人街探案2', '2018062418134600c0821f754a4b77876bf0104348d242.jpg', '2018-06-24 18:13:47');
INSERT INTO `preview` VALUES (5, '红海行动', '20180624181428334c4e11610546cab6f5824b98071467.jpg', '2018-06-24 18:14:28');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `auths` varchar(600) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `ix_role_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (1, 'admin', '1,2,3,4', '2018-01-18 22:05:47');
INSERT INTO `role` VALUES (2, '标签管理员', '1,2,3,4', '2018-01-23 20:59:00');
INSERT INTO `role` VALUES (3, '标签管理员1', '1,2,3', '2018-01-23 21:05:02');

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_tag_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES (1, '爱情', '2018-01-19 20:44:52');
INSERT INTO `tag` VALUES (2, '动作', '2018-01-19 20:58:20');
INSERT INTO `tag` VALUES (3, '科幻', '2018-01-19 21:30:07');
INSERT INTO `tag` VALUES (7, '喜剧', '2018-01-22 20:46:30');
INSERT INTO `tag` VALUES (8, '伦理', '2018-01-22 20:46:50');
INSERT INTO `tag` VALUES (9, '情色', '2018-01-26 17:17:03');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pwd` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `info` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `face` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  `uuid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE,
  UNIQUE INDEX `face`(`face`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  UNIQUE INDEX `phone`(`phone`) USING BTREE,
  UNIQUE INDEX `uuid`(`uuid`) USING BTREE,
  INDEX `ix_user_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'Devil', '12345678', '1063944784@qq.com', '13126051488', '我是大帅哥', '201801212011300c0ca6d33e9245339b757436d9eec350.jpg', '2018-01-21 20:09:49', '0c461f1e53164b6d95312a191aacb758');
INSERT INTO `user` VALUES (2, 'js_chen', 'pbkdf2:sha256:50000$czrqakGp$16285a688ab787acdd101d14e46f26c8a112f9768401faa9cf5f118504c60475', '12345678@qq.com', '13126051483', '我很帅', '20180126172244616e8f5cdfdc4d6281b0337aad7e53a4.jpg', '2018-01-25 20:47:56', '8ed099e124d74a96a4edbd8d53ab91de');

-- ----------------------------
-- Table structure for userlog
-- ----------------------------
DROP TABLE IF EXISTS `userlog`;
CREATE TABLE `userlog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `ip` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_userlog_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of userlog
-- ----------------------------
INSERT INTO `userlog` VALUES (1, 1, '127.0.0.1', '2018-01-22 21:13:18');
INSERT INTO `userlog` VALUES (2, 2, '127.0.0.1', '2018-01-25 21:00:27');
INSERT INTO `userlog` VALUES (3, 2, '127.0.0.1', '2018-01-25 21:07:08');
INSERT INTO `userlog` VALUES (4, 2, '127.0.0.1', '2018-01-25 21:07:58');
INSERT INTO `userlog` VALUES (5, 2, '127.0.0.1', '2018-01-26 16:23:51');
INSERT INTO `userlog` VALUES (6, 2, '127.0.0.1', '2018-01-26 19:56:18');
INSERT INTO `userlog` VALUES (7, 2, '127.0.0.1', '2018-01-27 20:58:05');

SET FOREIGN_KEY_CHECKS = 1;

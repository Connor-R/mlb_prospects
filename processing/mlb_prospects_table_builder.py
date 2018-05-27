from py_db import db

#Creates MySQL tables for the mlb_prospects database

#This is an initialization script, and only needs to be run once, prior to running every other script


db = db('mlb_prospects')

q = """
-- Create syntax for TABLE '2013_prospects'
CREATE TABLE `2013_prospects` (
  `prospect_id` int(11) unsigned NOT NULL DEFAULT '0',
  `mlb_id` int(11) NOT NULL,
  `mlb_draft_id` varchar(64) DEFAULT NULL,
  `mlb_international_id` varchar(64) DEFAULT NULL,
  `fg_minor_id` varchar(64) DEFAULT NULL,
  `fg_major_id` int(11) DEFAULT NULL,
  `*bio*` varchar(1) NOT NULL DEFAULT '',
  `first_name` varchar(64) DEFAULT NULL,
  `last_name` varchar(64) DEFAULT NULL,
  `age` decimal(11,2) DEFAULT NULL,
  `position` varchar(16) DEFAULT NULL,
  `bats` varchar(8) DEFAULT NULL,
  `throws` varchar(8) DEFAULT NULL,
  `height` varchar(11) DEFAULT NULL,
  `weight` varchar(11) DEFAULT NULL,
  `p_type` varchar(12) NOT NULL DEFAULT '',
  `avg_FV` decimal(22,1) DEFAULT NULL,
  `*fg*` varchar(1) NOT NULL DEFAULT '',
  `fg100` int(11) DEFAULT NULL,
  `fg_team` varchar(32) DEFAULT '',
  `fg_teamRank` int(11) DEFAULT NULL,
  `fg_position` varchar(16) DEFAULT '',
  `fg_signed` varchar(64) DEFAULT NULL,
  `fg_signedFrom` varchar(64) DEFAULT NULL,
  `fg_eta` int(11) DEFAULT NULL,
  `fg_FV` int(11) DEFAULT '0',
  `*mi*` varchar(1) NOT NULL DEFAULT '',
  `mi_team` varchar(32) DEFAULT '',
  `mi_teamRank` int(11) DEFAULT NULL,
  `mi_grade` varchar(16) DEFAULT NULL,
  `mi_FV` int(11) DEFAULT NULL,
  `*mlb*` varchar(1) NOT NULL DEFAULT '',
  `mlbp_top100` int(11) DEFAULT NULL,
  `mlbp_team` varchar(32) DEFAULT '',
  `mlbp_drafted` varchar(32) DEFAULT '',
  `mlbp_signed` varchar(32) DEFAULT '',
  `mlbp_eta` int(11) DEFAULT NULL,
  `mlbp_FV` int(11) DEFAULT '0',
  `*fg_draft*` varchar(1) NOT NULL DEFAULT '',
  `fgd_rank` int(11) DEFAULT NULL,
  `fgd_school` varchar(64) DEFAULT NULL,
  `fgd_FV` int(11) DEFAULT NULL,
  `*mlb_draft*` varchar(1) NOT NULL DEFAULT '',
  `mlbd_rank` int(11) DEFAULT NULL,
  `mlbd_school` varchar(64) DEFAULT NULL,
  `mlbd_grade` varchar(64) DEFAULT NULL,
  `mlbd_FV` int(11) DEFAULT '0',
  `*extras*` varchar(1) NOT NULL DEFAULT '',
  `fg_video` text,
  `mi_blurb` text,
  `mlbp_blurb` text,
  `fgd_video` text,
  `fgd_blurb` text,
  `mlbd_blurb` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE '2014_prospects'
CREATE TABLE `2014_prospects` (
  `prospect_id` int(11) unsigned NOT NULL DEFAULT '0',
  `mlb_id` int(11) NOT NULL,
  `mlb_draft_id` varchar(64) DEFAULT NULL,
  `mlb_international_id` varchar(64) DEFAULT NULL,
  `fg_minor_id` varchar(64) DEFAULT NULL,
  `fg_major_id` int(11) DEFAULT NULL,
  `*bio*` varchar(1) NOT NULL DEFAULT '',
  `first_name` varchar(64) DEFAULT NULL,
  `last_name` varchar(64) DEFAULT NULL,
  `age` decimal(11,2) DEFAULT NULL,
  `position` varchar(16) DEFAULT NULL,
  `bats` varchar(8) DEFAULT NULL,
  `throws` varchar(8) DEFAULT NULL,
  `height` varchar(11) DEFAULT NULL,
  `weight` varchar(11) DEFAULT NULL,
  `p_type` varchar(12) NOT NULL DEFAULT '',
  `avg_FV` decimal(22,1) DEFAULT NULL,
  `*fg*` varchar(1) NOT NULL DEFAULT '',
  `fg100` int(11) DEFAULT NULL,
  `fg_team` varchar(32) DEFAULT '',
  `fg_teamRank` int(11) DEFAULT NULL,
  `fg_position` varchar(16) DEFAULT '',
  `fg_signed` varchar(64) DEFAULT NULL,
  `fg_signedFrom` varchar(64) DEFAULT NULL,
  `fg_eta` int(11) DEFAULT NULL,
  `fg_FV` int(11) DEFAULT '0',
  `*mi*` varchar(1) NOT NULL DEFAULT '',
  `mi_team` varchar(32) DEFAULT '',
  `mi_teamRank` int(11) DEFAULT NULL,
  `mi_grade` varchar(16) DEFAULT NULL,
  `mi_FV` int(11) DEFAULT NULL,
  `*mlb*` varchar(1) NOT NULL DEFAULT '',
  `mlbp_top100` int(11) DEFAULT NULL,
  `mlbp_team` varchar(32) DEFAULT '',
  `mlbp_drafted` varchar(32) DEFAULT '',
  `mlbp_signed` varchar(32) DEFAULT '',
  `mlbp_eta` int(11) DEFAULT NULL,
  `mlbp_FV` int(11) DEFAULT '0',
  `*fg_draft*` varchar(1) NOT NULL DEFAULT '',
  `fgd_rank` int(11) DEFAULT NULL,
  `fgd_school` varchar(64) DEFAULT NULL,
  `fgd_FV` int(11) DEFAULT NULL,
  `*mlb_draft*` varchar(1) NOT NULL DEFAULT '',
  `mlbd_rank` int(11) DEFAULT NULL,
  `mlbd_school` varchar(64) DEFAULT NULL,
  `mlbd_grade` varchar(64) DEFAULT NULL,
  `mlbd_FV` int(11) DEFAULT '0',
  `*extras*` varchar(1) NOT NULL DEFAULT '',
  `fg_video` text,
  `mi_blurb` text,
  `mlbp_blurb` text,
  `fgd_video` text,
  `fgd_blurb` text,
  `mlbd_blurb` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE '2015_prospects'
CREATE TABLE `2015_prospects` (
  `prospect_id` int(11) unsigned NOT NULL DEFAULT '0',
  `mlb_id` int(11) NOT NULL,
  `mlb_draft_id` varchar(64) DEFAULT NULL,
  `mlb_international_id` varchar(64) DEFAULT NULL,
  `fg_minor_id` varchar(64) DEFAULT NULL,
  `fg_major_id` int(11) DEFAULT NULL,
  `*bio*` varchar(1) NOT NULL DEFAULT '',
  `first_name` varchar(64) DEFAULT NULL,
  `last_name` varchar(64) DEFAULT NULL,
  `age` decimal(11,2) DEFAULT NULL,
  `position` varchar(16) DEFAULT NULL,
  `bats` varchar(8) DEFAULT NULL,
  `throws` varchar(8) DEFAULT NULL,
  `height` varchar(11) DEFAULT NULL,
  `weight` varchar(11) DEFAULT NULL,
  `p_type` varchar(12) NOT NULL DEFAULT '',
  `avg_FV` decimal(22,1) DEFAULT NULL,
  `*fg*` varchar(1) NOT NULL DEFAULT '',
  `fg100` int(11) DEFAULT NULL,
  `fg_team` varchar(32) DEFAULT '',
  `fg_teamRank` int(11) DEFAULT NULL,
  `fg_position` varchar(16) DEFAULT '',
  `fg_signed` varchar(64) DEFAULT NULL,
  `fg_signedFrom` varchar(64) DEFAULT NULL,
  `fg_eta` int(11) DEFAULT NULL,
  `fg_FV` int(11) DEFAULT '0',
  `*mi*` varchar(1) NOT NULL DEFAULT '',
  `mi_team` varchar(32) DEFAULT '',
  `mi_teamRank` int(11) DEFAULT NULL,
  `mi_grade` varchar(16) DEFAULT NULL,
  `mi_FV` int(11) DEFAULT NULL,
  `*mlb*` varchar(1) NOT NULL DEFAULT '',
  `mlbp_top100` int(11) DEFAULT NULL,
  `mlbp_team` varchar(32) DEFAULT '',
  `mlbp_drafted` varchar(32) DEFAULT '',
  `mlbp_signed` varchar(32) DEFAULT '',
  `mlbp_eta` int(11) DEFAULT NULL,
  `mlbp_FV` int(11) DEFAULT '0',
  `*fg_draft*` varchar(1) NOT NULL DEFAULT '',
  `fgd_rank` int(11) DEFAULT NULL,
  `fgd_school` varchar(64) DEFAULT NULL,
  `fgd_FV` int(11) DEFAULT NULL,
  `*mlb_draft*` varchar(1) NOT NULL DEFAULT '',
  `mlbd_rank` int(11) DEFAULT NULL,
  `mlbd_school` varchar(64) DEFAULT NULL,
  `mlbd_grade` varchar(64) DEFAULT NULL,
  `mlbd_FV` int(11) DEFAULT '0',
  `*extras*` varchar(1) NOT NULL DEFAULT '',
  `fg_video` text,
  `mi_blurb` text,
  `mlbp_blurb` text,
  `fgd_video` text,
  `fgd_blurb` text,
  `mlbd_blurb` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE '2016_prospects'
CREATE TABLE `2016_prospects` (
  `prospect_id` int(11) unsigned NOT NULL DEFAULT '0',
  `mlb_id` int(11) NOT NULL,
  `mlb_draft_id` varchar(64) DEFAULT NULL,
  `mlb_international_id` varchar(64) DEFAULT NULL,
  `fg_minor_id` varchar(64) DEFAULT NULL,
  `fg_major_id` int(11) DEFAULT NULL,
  `*bio*` varchar(1) NOT NULL DEFAULT '',
  `first_name` varchar(64) DEFAULT NULL,
  `last_name` varchar(64) DEFAULT NULL,
  `age` decimal(11,2) DEFAULT NULL,
  `position` varchar(16) DEFAULT NULL,
  `bats` varchar(8) DEFAULT NULL,
  `throws` varchar(8) DEFAULT NULL,
  `height` varchar(11) DEFAULT NULL,
  `weight` varchar(11) DEFAULT NULL,
  `p_type` varchar(12) NOT NULL DEFAULT '',
  `avg_FV` decimal(22,1) DEFAULT NULL,
  `*fg*` varchar(1) NOT NULL DEFAULT '',
  `fg100` int(11) DEFAULT NULL,
  `fg_team` varchar(32) DEFAULT '',
  `fg_teamRank` int(11) DEFAULT NULL,
  `fg_position` varchar(16) DEFAULT '',
  `fg_signed` varchar(64) DEFAULT NULL,
  `fg_signedFrom` varchar(64) DEFAULT NULL,
  `fg_eta` int(11) DEFAULT NULL,
  `fg_FV` int(11) DEFAULT '0',
  `*mi*` varchar(1) NOT NULL DEFAULT '',
  `mi_team` varchar(32) DEFAULT '',
  `mi_teamRank` int(11) DEFAULT NULL,
  `mi_grade` varchar(16) DEFAULT NULL,
  `mi_FV` int(11) DEFAULT NULL,
  `*mlb*` varchar(1) NOT NULL DEFAULT '',
  `mlbp_top100` int(11) DEFAULT NULL,
  `mlbp_team` varchar(32) DEFAULT '',
  `mlbp_drafted` varchar(32) DEFAULT '',
  `mlbp_signed` varchar(32) DEFAULT '',
  `mlbp_eta` int(11) DEFAULT NULL,
  `mlbp_FV` int(11) DEFAULT '0',
  `*fg_draft*` varchar(1) NOT NULL DEFAULT '',
  `fgd_rank` int(11) DEFAULT NULL,
  `fgd_school` varchar(64) DEFAULT NULL,
  `fgd_FV` int(11) DEFAULT NULL,
  `*mlb_draft*` varchar(1) NOT NULL DEFAULT '',
  `mlbd_rank` int(11) DEFAULT NULL,
  `mlbd_school` varchar(64) DEFAULT NULL,
  `mlbd_grade` varchar(64) DEFAULT NULL,
  `mlbd_FV` int(11) DEFAULT '0',
  `*extras*` varchar(1) NOT NULL DEFAULT '',
  `fg_video` text,
  `mi_blurb` text,
  `mlbp_blurb` text,
  `fgd_video` text,
  `fgd_blurb` text,
  `mlbd_blurb` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE '2017_prospects'
CREATE TABLE `2017_prospects` (
  `prospect_id` int(11) unsigned NOT NULL DEFAULT '0',
  `mlb_id` int(11) NOT NULL,
  `mlb_draft_id` varchar(64) DEFAULT NULL,
  `mlb_international_id` varchar(64) DEFAULT NULL,
  `fg_minor_id` varchar(64) DEFAULT NULL,
  `fg_major_id` int(11) DEFAULT NULL,
  `*bio*` varchar(1) NOT NULL DEFAULT '',
  `first_name` varchar(64) DEFAULT NULL,
  `last_name` varchar(64) DEFAULT NULL,
  `age` decimal(11,2) DEFAULT NULL,
  `position` varchar(16) DEFAULT NULL,
  `bats` varchar(8) DEFAULT NULL,
  `throws` varchar(8) DEFAULT NULL,
  `height` varchar(11) DEFAULT NULL,
  `weight` varchar(11) DEFAULT NULL,
  `p_type` varchar(12) NOT NULL DEFAULT '',
  `avg_FV` decimal(22,1) DEFAULT NULL,
  `*fg*` varchar(1) NOT NULL DEFAULT '',
  `fg100` int(11) DEFAULT NULL,
  `fg_team` varchar(32) DEFAULT '',
  `fg_teamRank` int(11) DEFAULT NULL,
  `fg_position` varchar(16) DEFAULT '',
  `fg_signed` varchar(64) DEFAULT NULL,
  `fg_signedFrom` varchar(64) DEFAULT NULL,
  `fg_eta` int(11) DEFAULT NULL,
  `fg_FV` int(11) DEFAULT '0',
  `*mi*` varchar(1) NOT NULL DEFAULT '',
  `mi_team` varchar(32) DEFAULT '',
  `mi_teamRank` int(11) DEFAULT NULL,
  `mi_grade` varchar(16) DEFAULT NULL,
  `mi_FV` int(11) DEFAULT NULL,
  `*mlb*` varchar(1) NOT NULL DEFAULT '',
  `mlbp_top100` int(11) DEFAULT NULL,
  `mlbp_team` varchar(32) DEFAULT '',
  `mlbp_drafted` varchar(32) DEFAULT '',
  `mlbp_signed` varchar(32) DEFAULT '',
  `mlbp_eta` int(11) DEFAULT NULL,
  `mlbp_FV` int(11) DEFAULT '0',
  `*fg_draft*` varchar(1) NOT NULL DEFAULT '',
  `fgd_rank` int(11) DEFAULT NULL,
  `fgd_school` varchar(64) DEFAULT NULL,
  `fgd_FV` int(11) DEFAULT NULL,
  `*mlb_draft*` varchar(1) NOT NULL DEFAULT '',
  `mlbd_rank` int(11) DEFAULT NULL,
  `mlbd_school` varchar(64) DEFAULT NULL,
  `mlbd_grade` varchar(64) DEFAULT NULL,
  `mlbd_FV` int(11) DEFAULT '0',
  `*extras*` varchar(1) NOT NULL DEFAULT '',
  `fg_video` text,
  `mi_blurb` text,
  `mlbp_blurb` text,
  `fgd_video` text,
  `fgd_blurb` text,
  `mlbd_blurb` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE '2018_prospects'
CREATE TABLE `2018_prospects` (
  `prospect_id` int(11) unsigned NOT NULL DEFAULT '0',
  `mlb_id` int(11) NOT NULL,
  `mlb_draft_id` varchar(64) DEFAULT NULL,
  `mlb_international_id` varchar(64) DEFAULT NULL,
  `fg_minor_id` varchar(64) DEFAULT NULL,
  `fg_major_id` int(11) DEFAULT NULL,
  `*bio*` varchar(1) NOT NULL DEFAULT '',
  `first_name` varchar(64) DEFAULT NULL,
  `last_name` varchar(64) DEFAULT NULL,
  `age` decimal(11,2) DEFAULT NULL,
  `position` varchar(16) DEFAULT NULL,
  `bats` varchar(8) DEFAULT NULL,
  `throws` varchar(8) DEFAULT NULL,
  `height` varchar(11) DEFAULT NULL,
  `weight` varchar(11) DEFAULT NULL,
  `p_type` varchar(12) NOT NULL DEFAULT '',
  `avg_FV` decimal(22,1) DEFAULT NULL,
  `*fg*` varchar(1) NOT NULL DEFAULT '',
  `fg100` int(11) DEFAULT NULL,
  `fg_team` varchar(32) DEFAULT '',
  `fg_teamRank` int(11) DEFAULT NULL,
  `fg_position` varchar(16) DEFAULT '',
  `fg_signed` varchar(64) DEFAULT NULL,
  `fg_signedFrom` varchar(64) DEFAULT NULL,
  `fg_eta` int(11) DEFAULT NULL,
  `fg_FV` int(11) DEFAULT '0',
  `*mi*` varchar(1) NOT NULL DEFAULT '',
  `mi_team` varchar(32) DEFAULT '',
  `mi_teamRank` int(11) DEFAULT NULL,
  `mi_grade` varchar(16) DEFAULT NULL,
  `mi_FV` int(11) DEFAULT NULL,
  `*mlb*` varchar(1) NOT NULL DEFAULT '',
  `mlbp_top100` int(11) DEFAULT NULL,
  `mlbp_team` varchar(32) DEFAULT '',
  `mlbp_drafted` varchar(32) DEFAULT '',
  `mlbp_signed` varchar(32) DEFAULT '',
  `mlbp_eta` int(11) DEFAULT NULL,
  `mlbp_FV` int(11) DEFAULT '0',
  `*fg_draft*` varchar(1) NOT NULL DEFAULT '',
  `fgd_rank` int(11) DEFAULT NULL,
  `fgd_school` varchar(64) DEFAULT NULL,
  `fgd_FV` int(11) DEFAULT NULL,
  `*mlb_draft*` varchar(1) NOT NULL DEFAULT '',
  `mlbd_rank` int(11) DEFAULT NULL,
  `mlbd_school` varchar(64) DEFAULT NULL,
  `mlbd_grade` varchar(64) DEFAULT NULL,
  `mlbd_FV` int(11) DEFAULT '0',
  `*extras*` varchar(1) NOT NULL DEFAULT '',
  `fg_video` text,
  `mi_blurb` text,
  `mlbp_blurb` text,
  `fgd_video` text,
  `fgd_blurb` text,
  `mlbd_blurb` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'fg_grades_hitters'
CREATE TABLE `fg_grades_hitters` (
  `year` int(11) NOT NULL DEFAULT '0',
  `fg_id` varchar(64) NOT NULL DEFAULT '',
  `Hit_present` int(11) DEFAULT NULL,
  `Hit_future` int(11) DEFAULT NULL,
  `GamePower_present` int(11) DEFAULT NULL,
  `GamePower_future` int(11) DEFAULT NULL,
  `RawPower_present` int(11) DEFAULT NULL,
  `RawPower_future` int(11) DEFAULT NULL,
  `Speed_present` int(11) DEFAULT NULL,
  `Speed_future` int(11) DEFAULT NULL,
  `Field_present` int(11) DEFAULT NULL,
  `Field_future` int(11) DEFAULT NULL,
  `Throws_present` int(11) DEFAULT NULL,
  `Throws_future` int(11) DEFAULT NULL,
  PRIMARY KEY (`year`,`fg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'fg_grades_pitchers'
CREATE TABLE `fg_grades_pitchers` (
  `year` int(11) NOT NULL DEFAULT '0',
  `fg_id` varchar(64) NOT NULL DEFAULT '',
  `Fastball_present` int(11) DEFAULT NULL,
  `Fastball_future` int(11) DEFAULT NULL,
  `Changeup_present` int(11) DEFAULT NULL,
  `Changeup_future` int(11) DEFAULT NULL,
  `Curveball_present` int(11) DEFAULT NULL,
  `Curveball_future` int(11) DEFAULT NULL,
  `Slider_present` int(11) DEFAULT NULL,
  `Slider_future` int(11) DEFAULT NULL,
  `Cutter_present` int(11) DEFAULT NULL,
  `Cutter_future` int(11) DEFAULT NULL,
  `Splitter_present` int(11) DEFAULT NULL,
  `Splitter_future` int(11) DEFAULT NULL,
  `Other_present` int(11) DEFAULT NULL,
  `Other_future` int(11) DEFAULT NULL,
  `Command_present` int(11) DEFAULT NULL,
  `Command_future` int(11) DEFAULT NULL,
  PRIMARY KEY (`year`,`fg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'fg_prospects_draft'
CREATE TABLE `fg_prospects_draft` (
  `year` int(11) unsigned NOT NULL,
  `prospect_id` varchar(64) NOT NULL DEFAULT '0',
  `rank` int(11) DEFAULT NULL,
  `full_name` varchar(64) NOT NULL DEFAULT '',
  `fname` varchar(32) NOT NULL DEFAULT '',
  `lname` varchar(32) NOT NULL DEFAULT '',
  `draft_age` decimal(8,1) NOT NULL DEFAULT '0.0',
  `est_years` varchar(16) DEFAULT '',
  `school` varchar(64) DEFAULT NULL,
  `position` varchar(16) DEFAULT '',
  `bats` varchar(8) DEFAULT '',
  `throws` varchar(8) DEFAULT '',
  `height` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `fv` int(11) DEFAULT NULL,
  `video` text,
  `blurb` text,
  PRIMARY KEY (`year`,`prospect_id`,`fname`,`lname`,`draft_age`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'fg_prospects_international'
CREATE TABLE `fg_prospects_international` (
  `year` int(11) unsigned NOT NULL,
  `prospect_id` varchar(64) NOT NULL DEFAULT '0',
  `rank` int(11) DEFAULT NULL,
  `full_name` varchar(64) NOT NULL DEFAULT '',
  `fname` varchar(32) NOT NULL DEFAULT '',
  `lname` varchar(32) NOT NULL DEFAULT '',
  `j2_age` decimal(8,1) NOT NULL DEFAULT '0.0',
  `est_years` varchar(16) DEFAULT NULL,
  `country` varchar(64) DEFAULT NULL,
  `position` varchar(16) DEFAULT '',
  `bats` varchar(8) DEFAULT '',
  `throws` varchar(8) DEFAULT '',
  `height` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `risk` int(11) DEFAULT NULL,
  `fv` int(11) DEFAULT NULL,
  `proj_team` varchar(32) DEFAULT NULL,
  `video` text,
  `blurb` text,
  PRIMARY KEY (`year`,`prospect_id`,`fname`,`lname`,`j2_age`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'fg_prospects_professional'
CREATE TABLE `fg_prospects_professional` (
  `year` int(11) unsigned NOT NULL,
  `prospect_id` int(11) NOT NULL DEFAULT '0',
  `fg_id` varchar(64) NOT NULL DEFAULT '',
  `top100` int(11) DEFAULT NULL,
  `team_rank` int(11) DEFAULT NULL,
  `full_name` varchar(64) DEFAULT '',
  `fname` varchar(32) DEFAULT '',
  `lname` varchar(32) DEFAULT '',
  `birth_year` int(11) DEFAULT NULL,
  `birth_month` int(11) DEFAULT NULL,
  `birth_day` int(11) DEFAULT NULL,
  `signed` varchar(64) DEFAULT NULL,
  `signed_from` varchar(64) DEFAULT NULL,
  `team` varchar(32) DEFAULT '',
  `position` varchar(16) DEFAULT '',
  `bats` varchar(8) DEFAULT '',
  `throws` varchar(8) DEFAULT '',
  `height` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `eta` int(11) DEFAULT NULL,
  `FV` int(11) NOT NULL DEFAULT '0',
  `video` text,
  PRIMARY KEY (`year`,`prospect_id`,`fg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'minorleagueball_professional'
CREATE TABLE `minorleagueball_professional` (
  `year` int(11) NOT NULL DEFAULT '0',
  `prospect_id` int(11) NOT NULL DEFAULT '0',
  `team` varchar(32) NOT NULL DEFAULT '',
  `team_rank` int(11) DEFAULT NULL,
  `full_name` varchar(64) NOT NULL DEFAULT '',
  `position` varchar(16) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `grade` varchar(16) DEFAULT NULL,
  `eta` varchar(64) DEFAULT NULL,
  `fname` varchar(32) NOT NULL DEFAULT '',
  `lname` varchar(32) NOT NULL DEFAULT '',
  `FV` int(11) DEFAULT NULL,
  `blurb` text,
  PRIMARY KEY (`year`,`team`,`fname`,`lname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'mlb_grades_hitters'
CREATE TABLE `mlb_grades_hitters` (
  `year` int(11) NOT NULL DEFAULT '0',
  `mlb_id` varchar(64) NOT NULL DEFAULT '',
  `prospect_type` varchar(32) NOT NULL DEFAULT '',
  `hit` int(11) DEFAULT NULL,
  `power` int(11) DEFAULT NULL,
  `run` int(11) DEFAULT NULL,
  `arm` int(11) DEFAULT NULL,
  `field` int(11) DEFAULT NULL,
  PRIMARY KEY (`year`,`mlb_id`,`prospect_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'mlb_grades_pitchers'
CREATE TABLE `mlb_grades_pitchers` (
  `year` int(11) NOT NULL DEFAULT '0',
  `mlb_id` varchar(64) NOT NULL DEFAULT '',
  `prospect_type` varchar(32) NOT NULL DEFAULT '',
  `fastball` int(11) DEFAULT NULL,
  `change` int(11) DEFAULT NULL,
  `curve` int(11) DEFAULT NULL,
  `slider` int(11) DEFAULT NULL,
  `cutter` int(11) DEFAULT NULL,
  `splitter` int(11) DEFAULT NULL,
  `other` int(11) DEFAULT NULL,
  `control` int(11) DEFAULT NULL,
  PRIMARY KEY (`year`,`mlb_id`,`prospect_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'mlb_prospects_draft'
CREATE TABLE `mlb_prospects_draft` (
  `year` int(11) unsigned NOT NULL,
  `prospect_id` int(11) NOT NULL DEFAULT '0',
  `mlb_id` varchar(64) NOT NULL DEFAULT '',
  `rank` int(11) DEFAULT NULL,
  `fname` varchar(32) DEFAULT '',
  `lname` varchar(32) DEFAULT '',
  `birth_year` int(11) DEFAULT NULL,
  `birth_month` int(11) DEFAULT NULL,
  `birth_day` int(11) DEFAULT NULL,
  `school_city` varchar(64) DEFAULT NULL,
  `grade_country` varchar(64) DEFAULT NULL,
  `college_commit` varchar(64) DEFAULT NULL,
  `team` varchar(32) DEFAULT '',
  `position` varchar(16) DEFAULT '',
  `bats` varchar(8) DEFAULT '',
  `throws` varchar(8) DEFAULT '',
  `height` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `drafted` varchar(32) DEFAULT '',
  `signed` int(11) DEFAULT NULL,
  `pre_top100` int(11) DEFAULT NULL,
  `eta` int(11) DEFAULT NULL,
  `FV` int(11) NOT NULL DEFAULT '0',
  `twitter` varchar(32) DEFAULT '',
  `blurb` text,
  PRIMARY KEY (`year`,`prospect_id`,`mlb_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'mlb_prospects_international'
CREATE TABLE `mlb_prospects_international` (
  `year` int(11) unsigned NOT NULL,
  `prospect_id` int(11) NOT NULL DEFAULT '0',
  `mlb_id` varchar(64) NOT NULL DEFAULT '',
  `rank` int(11) DEFAULT NULL,
  `fname` varchar(32) DEFAULT '',
  `lname` varchar(32) DEFAULT '',
  `birth_year` int(11) DEFAULT NULL,
  `birth_month` int(11) DEFAULT NULL,
  `birth_day` int(11) DEFAULT NULL,
  `school_city` varchar(64) DEFAULT NULL,
  `grade_country` varchar(64) DEFAULT NULL,
  `college_commit` varchar(64) DEFAULT NULL,
  `team` varchar(32) DEFAULT '',
  `position` varchar(16) DEFAULT '',
  `bats` varchar(8) DEFAULT '',
  `throws` varchar(8) DEFAULT '',
  `height` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `drafted` varchar(32) DEFAULT '',
  `signed` int(11) DEFAULT NULL,
  `pre_top100` int(11) DEFAULT NULL,
  `eta` int(11) DEFAULT NULL,
  `FV` int(11) NOT NULL DEFAULT '0',
  `twitter` varchar(32) DEFAULT '',
  `blurb` text,
  PRIMARY KEY (`year`,`prospect_id`,`mlb_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'mlb_prospects_professional'
CREATE TABLE `mlb_prospects_professional` (
  `year` int(11) unsigned NOT NULL,
  `prospect_id` int(11) NOT NULL DEFAULT '0',
  `mlb_id` int(11) NOT NULL,
  `rank` int(11) DEFAULT NULL,
  `fname` varchar(32) DEFAULT '',
  `lname` varchar(32) DEFAULT '',
  `birth_year` int(11) DEFAULT NULL,
  `birth_month` int(11) DEFAULT NULL,
  `birth_day` int(11) DEFAULT NULL,
  `school_city` varchar(64) DEFAULT NULL,
  `grade_country` varchar(64) DEFAULT NULL,
  `college_commit` varchar(64) DEFAULT NULL,
  `team` varchar(32) DEFAULT '',
  `position` varchar(16) DEFAULT '',
  `bats` varchar(8) DEFAULT '',
  `throws` varchar(8) DEFAULT '',
  `height` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `drafted` varchar(32) DEFAULT '',
  `signed` varchar(32) DEFAULT '',
  `pre_top100` int(11) DEFAULT NULL,
  `eta` int(11) DEFAULT NULL,
  `FV` int(11) NOT NULL DEFAULT '0',
  `twitter` varchar(32) DEFAULT '',
  `blurb` text,
  PRIMARY KEY (`year`,`prospect_id`,`mlb_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create syntax for TABLE 'professional_prospects'
CREATE TABLE `professional_prospects` (
  `prospect_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `birth_year` int(11) DEFAULT NULL,
  `birth_month` int(11) DEFAULT NULL,
  `birth_day` int(11) DEFAULT NULL,
  `mlb_id` int(11) NOT NULL,
  `mlb_draft_id` varchar(64) DEFAULT NULL,
  `mlb_international_id` varchar(64) DEFAULT NULL,
  `fg_minor_id` varchar(64) DEFAULT NULL,
  `fg_major_id` int(11) DEFAULT NULL,
  `mlb_fname` varchar(64) DEFAULT NULL,
  `mlb_lname` varchar(64) DEFAULT NULL,
  `fg_fname` varchar(64) DEFAULT NULL,
  `fg_lname` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`prospect_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2698 DEFAULT CHARSET=latin1;
"""

db.query(q)


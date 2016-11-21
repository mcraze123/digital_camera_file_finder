#!/usr/bin/perl
use strict;
use warnings;
use File::Find;

if($#ARGV != 0){
	print "Usage: ./finddc.pl <system_drive>\n";
	print "E.g.\n";
	print " ./finddc.pl C:\n";
	exit 1;
}

print "Searching $ARGV[0] for camera files...\n";

find({
	preprocess => \&preprocess,
	wanted => \&wanted
}, $ARGV[0]);

sub preprocess {
	my @list;
	foreach (@_){
		if( -d && $_ =~ m/DCIM/){ push @list, $_; }
		
		# .wav files are ommitted in the search
		if(-f && $_ =~ m/(DSC_|IMG_)\d+(\.jpg|\.tif|\.thm|\.png)/i){
			print "$_\n";
			push @list, $_;
		}
		
		# file names list came from:
		# http://diddly.com/random/about.html
		# Kodak
		if(-f && $_ =~ m/dcp\d+\.jpg/i){ push @list, $_; }

		# Nikon
		if(-f && $_ =~ m/dsc[n]?\d+\.jpg/i){ push @list, $_; }
		
		# Sony
		if(-f && $_ =~ m/mvc[-]?\d+\.jpg/i){ push @list, $_; }
		
		# Olympus
		if(-f && $_ =~ m/P(101|MDD)\d+\.jpg/i){ push @list, $_; }

		# RCA and Samsung
		if(-f && $_ =~ m/IM[A]?G\d+\.jpg/i){ push @list, $_; }

		# Canon
		if(-f && $_ =~ m/1\d+-\d+(_IMG)?\.jpg/i){ push @list, $_; }
		if(-f && $_ =~ m/(I|_)MG_\d+\.jpg/i){ push @list, $_; }
		
		# Fuji Finepix
		if(-f && $_ =~ m/dscf\d+\.jpg/i){ push @list, $_; }

		# Toshiba PDR
		if(-f && $_ =~ m/pdrm\d+\.jpg/i){ push @list, $_; }

		# HP Photosmart
		if(-f && $_ =~ m/(IM|EX)\d+\.jpg/i){ push @list, $_; }

		# Kodak DC-40,50,120, S is (L)arge (M)edium (S)mall.
		if(-f && $_ =~ m/DC\d+(L|M|S)\.jpg/i){ push @list, $_; }

		# Minolta Dimage
		if(-f && $_ =~ m/pict\d+\.jpg/i){ push @list, $_; }

		# Kodak DC290
		if(-f && $_ =~ m/P\d+\.JPG/i){ push @list, $_; }

		# Casio
		if(-f && $_ =~ m/(YYMDD|MMDD)\d+\.JPG/i){ push @list, $_; }
		
		# Pentax
		if(-f && $_ =~ m/IMGP\d+\.JPG/i){ push @list, $_; }

		# Panasonic
		if(-f && $_ =~ m/PANA\d+\.JPG/i){ push @list, $_; }

		# HTC Desire Z/Tmobil G2
		if(-f && $_ =~ m/IMG_\d{8}_\d{6}.JPG/i){ push @list, $_; }

		# Facebook
		if(-f && $_ =~ m/\d+_\d+_\d+_n.jpg/i){ push @list, $_; }

	}
	return @list;
}

sub wanted {
	foreach (@_){
		print "$_\n";
	}
	print "done...\n";
}

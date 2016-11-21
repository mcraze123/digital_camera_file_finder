#!/usr/bin/perl
use strict;
use warnings;
use File::Find::Rule;
use File::Find::Rule::MMagic;
use File::Find::Rule::ImageSize;

if($#ARGV < 0){
	print "usage: ./ppf.pl <directories>\n";
	exit 1;
}

my $rule=File::Find::Rule->new;
$rule->file;
$rule->name('*.jpg','*.jpeg','*.png','*.tif','*.tiff'); # check extension
$rule->magic('image/*'); # check the mime type
$rule->image_x('>300'); # pictures will be >=320x240
$rule->image_y('>200');
my @imgz=$rule->in(@ARGV);

foreach my $i (@imgz){
	print "$i\n";
}

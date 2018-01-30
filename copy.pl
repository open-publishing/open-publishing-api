#!/usr/bin/perl


use strict;
my $ng_root = $ENV{'NG_ROOT'};

if(length($ng_root)==0)
{
	die "Please set NG_ROOT environment variable.\n";
}

my @FILES = split /\n/, `find $ng_root/../python/open_publishing|grep -v __pycache__`;

print `rm ./open_publishing/*/*.py`;
print `rm ./open_publishing/*.py`;

foreach(@FILES)
{
	my $orig = $_;
	my $local = $orig;
	$local=~s/^.*python\///;
	print "$orig -> $local\n"; 

	if (-d $orig)
	{
		print `mkdir -p $local`;
	}
	else
	{
    		print `cp $orig $local`;
	}
}


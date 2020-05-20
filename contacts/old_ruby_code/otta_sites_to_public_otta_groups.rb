#!/usr/bin/env ruby

require 'builder'

EXPECTED_HEADER="Studies	OTTA Study Acronym	OCAC Site	Study Name		Primary contact	other contacts	other contacts	other contacts	other contacts	other contacts	other contactsother contacts	other contacts	email address	email address	email address	email address	email address	email address	email address	email address	email address"

excluded_groups = Array.new
excluded_groups.push("ARL")
excluded_groups.push("COE")

def clean(str)
   str.strip.gsub(/\"/, "")
end

data = Array.new
line_count = 0
while (line = gets)
   line_count += 1
   if (line_count == 1)
      if (line != EXPECTED_HEADER)
         STDERR.puts "Header not expected and I make assumptions of column numbers based on this header"
         STDERR.puts EXPECTED_HEADER
         STDERR.puts line
         #exit 1
         next
      end   
   end
   fields = line.split(/\t/)
   otta_study_acronym = clean(fields[1])
   next if excluded_groups.include?(otta_study_acronym)
   ocac_site = clean(fields[2])
   study_name = clean(fields[3])
   primary_contact = clean(fields[5])
   primary_contact_email = clean(fields[14])
   data.clear
   data.push(otta_study_acronym)
   data.push(study_name)
   data.push(primary_contact)
   data.push(primary_contact_email)
   data.push(ocac_site)
   puts data.join("\t")
end
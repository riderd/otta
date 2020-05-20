#!/usr/bin/env ruby

excluded_groups = Array.new
excluded_groups.push("ARL")
excluded_groups.push("COE")

def clean(str)
   str.strip.gsub(/\"/, "")
end

def read_ocac(filename)
   otta_ocac_map = Hash.new
   File.foreach(filename) do |line|
      fields = line.strip.split(/\t/)
      next if fields.empty?
      if (fields.size > 3)
         STDERR.puts "#{line} has more fields than I expected"
         exit 1
      end
      ocac = nil
      ocac = fields[2].strip if (fields.size == 3)
      otta_ocac_map[fields[0]] = ocac  
      # Only for debugging purposes - otherwise comment out as it messes up
      # downstream processing
      #puts line
   end
   otta_ocac_map
end

def read_description(filename)
   otta_descriptions = Hash.new
   File.foreach(filename) do |line|
      fields = line.strip.split(/\t/)
      next if fields.empty?
      if (fields.size > 3)
         STDERR.puts "#{line} has more fields than I expected"
         exit 1
      end
      description = nil
      description = fields[1].strip if (fields.size > 1)
      otta_descriptions[fields[0]] = description  
   end
   otta_descriptions
end

otta_description_ocac_filename = ARGV.shift

otta_ocac_map = read_ocac(otta_description_ocac_filename)

otta_descriptions = read_description(otta_description_ocac_filename)

data = Array.new
line_count = 0
while (line = gets)
   fields = line.split(/\t/)
   otta_study_acronym = clean(fields[0])
   next if excluded_groups.include?(otta_study_acronym)
   next if (fields[1].strip().downcase() != "yes")   
   primary_contact = clean(fields[2])
   primary_contact_email = clean(fields[3])
   data.clear
   description = otta_descriptions[otta_study_acronym]
   description = "" if description.nil?
   if (description == "")
      STDERR.puts "Don't have description for otta study #{otta_study_acronym}"
   end
   ocac_acronym = otta_ocac_map[otta_study_acronym]
   ocac_acronym = "" if ocac_acronym.nil?
   if (ocac_acronym == "")
      STDERR.puts "Don't have ocac acronym for otta study #{otta_study_acronym}"
   end
   data.push(otta_study_acronym)
   data.push(description)
   data.push(primary_contact)
   data.push(primary_contact_email)
   data.push(ocac_acronym)
   puts data.join("\t")
end

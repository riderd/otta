#!/usr/bin/env ruby

require 'builder'

header = ARGV.shift
header_fields = header.split(/,/)

table_class = ARGV.shift

rows = Array.new()
while (line = gets)
   fields = line.strip.split(/\t/)
   next if (fields.size == 0)
   if (fields.size != header_fields.size)
      STDERR.puts "#{line.strip} (#{fields.size} fields) doesnt match headers (#{header_fields.size} fields) in number of fields"
      exit 1
   end
   row = Array.new
   fields.each() do |field|
      row.push(field.strip)
   end
   rows.push(row)
end
   
html = Builder::XmlMarkup.new(:indent => 2)
html.table(class: table_class) {
   html.thead { html.tr { header_fields.each{ |h| html.th(h) } } }
   html.tbody {
      rows.each() do |row|
         html.tr { row.each() {|val| html.td(val) } }
      end
   }
}
puts "#{html}"

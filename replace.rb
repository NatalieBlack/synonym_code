require 'json'
require 'open-uri'

def synonym(word)
  begin
    results = {}
    open("http://words.bighugelabs.com/api/2/e47598ad741728aecaa3bd6a5a35630c/#{word}/json") do |f|
      f.each_line do |line|
        results = JSON.parse(line).first.last
      end
    end 
    return results['syn'].first
  rescue
    return word
  end
end

lang = ARGV[0]
langs = ["ruby"]
unless langs.include? lang
  puts "Invalid language option.  Supported language options include: #{langs}"
  exit
end

keys = File.open("keywords/#{lang}.txt")

srcfn = ARGV[1]
src = File.open(srcfn)

kws = []

IO.foreach(keys) do |line|
  kws << line.strip
end

IO.foreach(src) do |line|
  line.split(" ").each do |word|
    if kws.include? word.strip
      line.gsub!(" #{word} ", " #{synonym(word.strip)} ")
    end
  end
  puts line
end

keys.close
src.close

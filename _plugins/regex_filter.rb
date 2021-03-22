module Jekyll
  module RegexFilter
    def replace_regex(input, regex_string, replacement)
      regex = Regexp.new regex_string
      input.gsub(regex, replacement)
    end
  end
end

Liquid::Template.register_filter(Jekyll::RegexFilter)
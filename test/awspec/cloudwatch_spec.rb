# aws spec testing lambda event cloudwatch

require 'awspec'
require 'aws-sdk'
require 'rhcl'

cloudwatch_name = ['trigger-lambda-nuke-everything']

cloudwatch_name.each do |name|
  describe cloudwatch_event(name) do
    it { should exist }
    it { should be_enable }
  end
end

# aws spec testing iam lambda sheduler

require 'awspec'
require 'aws-sdk'
require 'rhcl'

role_name = 'everything-lambda-nuke'

describe iam_role(role_name) do
  it { should exist }
  it { should have_inline_policy }
end

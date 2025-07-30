class Trmd < Formula
  include Language::Python::Virtualenv

  desc "Translate Markdown using OpenAI"
  homepage "https://github.com/rioriost/homebrew-trmd/"
  url "https://files.pythonhosted.org/packages/10/cc/c5c2e04ef3d48df283aa605a726dea13e45c32af4739447bcb769ad04ce8/trmd-0.1.6.tar.gz"
  sha256 "fb0b457aea4ef7641e0f1e00db1f33daef178398160c675684db28f0c23fee93"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
    system libexec/"bin/python", "-m", "pip", "install", "openai"
  end

  test do
    system "#{bin}/trmd", "--help"
  end
end

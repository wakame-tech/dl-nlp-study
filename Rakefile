
namespace :mercari do
  task :run do
    sh 'streamlit run mercari/index.py'
  end
end

namespace :vtuber do
  file 'data/vtuber_movies_20191030.csv' do
    cd 'dataset' do
      sh 'curl gdrive.sh | bash -s 1fW4M4u_GzM2VXk-JPOv1CQ64ZX-71_1T'
    end
  end

  task :dataset => ['data/vtuber_movies_20191030.csv'] do
    puts "📚 Downloaded Vtuber Dataset"
  end

  desc '💿 Do Preprocess'
  task :preprocess do |t|
    puts '💿 Do Preprocess'
    # preprocess
    sh 'ROOT=`pwd` python vtuber/preprocess.py'
  end
end
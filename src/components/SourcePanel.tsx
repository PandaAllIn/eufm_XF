import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

interface FileNode {
  name: string;
  path: string;
  type: 'file' | 'directory';
  children?: FileNode[];
}

interface TreeProps {
  node: FileNode;
  onFileClick: (path: string) => void;
}

const TreeNode: React.FC<TreeProps> = ({ node, onFileClick }) => {
  const [open, setOpen] = useState(false);

  if (node.type === 'directory') {
    return (
      <div>
        <div onClick={() => setOpen(!open)} style={{ cursor: 'pointer' }}>
          {open ? '📂' : '📁'} {node.name}
        </div>
        {open && node.children && (
          <div style={{ paddingLeft: 16 }}>
            {node.children.map((child) => (
              <TreeNode key={child.path} node={child} onFileClick={onFileClick} />
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <div onClick={() => onFileClick(node.path)} style={{ cursor: 'pointer' }}>
      📄 {node.name}
    </div>
  );
};

const SourcePanel: React.FC = () => {
  const [tree, setTree] = useState<FileNode[]>([]);
  const [content, setContent] = useState('');
  const [activePath, setActivePath] = useState('');

  useEffect(() => {
    fetch('/api/collaboration/files')
      .then((res) => res.json())
      .then(setTree)
      .catch(() => setTree([]));
  }, []);

  const handleFileClick = async (path: string) => {
    const res = await fetch(`/api/collaboration/file?path=${encodeURIComponent(path)}`);
    if (res.ok) {
      const data = await res.json();
      setActivePath(path);
      setContent(data.content);
    }
  };

  const isMarkdown = activePath.endsWith('.md');

  return (
    <div style={{ display: 'flex', height: '100%' }}>
      <div style={{ width: '30%', overflowY: 'auto', paddingRight: 16 }}>
        {tree.map((node) => (
          <TreeNode key={node.path} node={node} onFileClick={handleFileClick} />
        ))}
      </div>
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {isMarkdown ? (
          <ReactMarkdown>{content}</ReactMarkdown>
        ) : (
          <pre>
            <code>{content}</code>
          </pre>
        )}
      </div>
    </div>
  );
};

export default SourcePanel;

